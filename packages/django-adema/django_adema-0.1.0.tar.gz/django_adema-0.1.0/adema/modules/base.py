"""
ADEMA Module Base Classes
=========================

Clases base para definir módulos acoplables a ADEMA.

Cada módulo externo (adema-ventas, adema-compras, etc.) debe:
1. Heredar de AdemaModule
2. Definir su ModuleMetadata
3. Registrarse via entry_points en setup.py/pyproject.toml

Estructura de un módulo:
    adema_ventas/
    ├── module.py              # Clase VentasModule (auto-descubre entidades)
    ├── models/                # Un archivo por entidad
    │   ├── __init__.py
    │   ├── venta.py           # class Venta(AdemaBaseModel)
    │   ├── linea_venta.py
    │   └── cliente.py
    ├── admin/                 # Un archivo por entidad
    │   ├── __init__.py
    │   ├── venta_admin.py
    │   └── cliente_admin.py
    ├── services/              # Un archivo por servicio
    │   ├── __init__.py
    │   ├── venta_service.py
    │   └── cliente_service.py
    └── views/
        └── ...

Ejemplo de módulo con auto-descubrimiento:
    
    # En adema_ventas/module.py
    from adema.modules import AdemaModule, ModuleMetadata
    
    class VentasModule(AdemaModule):
        metadata = ModuleMetadata(
            name="ventas",
            label="Ventas",
            description="Módulo de gestión de ventas",
            version="0.1.0",
        )
        # No es necesario definir get_models(), get_admin_classes(), etc.
        # El módulo auto-descubre las entidades en las carpetas correspondientes
"""

import os
import importlib
import inspect
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Type
from abc import ABC


@dataclass
class ModuleMetadata:
    """
    Metadatos de un módulo ADEMA.
    
    Attributes:
        name: Identificador único del módulo (snake_case)
        label: Nombre legible para mostrar en UI
        description: Descripción del módulo
        version: Versión del módulo (semver)
        author: Autor o equipo del módulo
        django_app: Nombre de la app Django (para INSTALLED_APPS)
        dependencies: Lista de dependencias requeridas
        icon: Icono para mostrar en UI (emoji o clase CSS)
        category: Categoría del módulo (erp, crm, utils, etc.)
        tags: Tags para búsqueda y filtrado
        documentation_url: URL a la documentación
        repository_url: URL al repositorio
    """
    name: str
    label: str
    description: str = ""
    version: str = "0.1.0"
    author: str = ""
    django_app: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    icon: str = "📦"
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    documentation_url: Optional[str] = None
    repository_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para serialización JSON."""
        return {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "django_app": self.django_app or f"adema_{self.name}",
            "dependencies": self.dependencies,
            "icon": self.icon,
            "category": self.category,
            "tags": self.tags,
            "documentation_url": self.documentation_url,
            "repository_url": self.repository_url,
        }


class AdemaModule(ABC):
    """
    Clase base abstracta para módulos ADEMA.
    
    Soporta auto-descubrimiento de entidades en carpetas:
    - models/     → Modelos Django (clases que heredan de AdemaBaseModel)
    - admin/      → Clases ModelAdmin
    - services/   → Clases de servicios de negocio
    - views/      → Vistas
    
    Ejemplo mínimo:
        class VentasModule(AdemaModule):
            metadata = ModuleMetadata(
                name="ventas",
                label="Ventas",
                description="Gestión de ventas",
            )
        # Eso es todo! El módulo auto-descubre models/, admin/, services/
    """
    
    # Metadatos del módulo (debe ser definido por subclases)
    metadata: ModuleMetadata = None
    
    # Cache de entidades descubiertas
    _discovered_models: List[Any] = None
    _discovered_admins: List[Any] = None
    _discovered_services: List[Any] = None
    
    def __init__(self):
        """Inicializar el módulo."""
        if self.metadata is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} debe definir 'metadata' "
                "como un ModuleMetadata"
            )
        # Resetear cache
        self._discovered_models = None
        self._discovered_admins = None
        self._discovered_services = None
    
    @property
    def name(self) -> str:
        """Nombre del módulo."""
        return self.metadata.name
    
    @property
    def label(self) -> str:
        """Label legible del módulo."""
        return self.metadata.label
    
    @property
    def version(self) -> str:
        """Versión del módulo."""
        return self.metadata.version
    
    @property
    def django_app(self) -> str:
        """Nombre de la app Django para INSTALLED_APPS."""
        return self.metadata.django_app or f"adema_{self.metadata.name}"
    
    def _get_module_path(self) -> Optional[Path]:
        """Obtiene el path del directorio del módulo."""
        try:
            module = importlib.import_module(self.django_app)
            if hasattr(module, '__file__') and module.__file__:
                return Path(module.__file__).parent
        except ImportError:
            pass
        return None
    
    def _discover_in_folder(
        self, 
        folder_name: str, 
        base_class: Optional[Type] = None,
        base_class_name: Optional[str] = None
    ) -> List[Any]:
        """
        Auto-descubre clases en una carpeta del módulo.
        
        Args:
            folder_name: Nombre de la carpeta (models, admin, services)
            base_class: Clase base que deben heredar (opcional)
            base_class_name: Nombre de la clase base como string (para imports lazy)
            
        Returns:
            Lista de clases descubiertas
        """
        discovered = []
        module_path = self._get_module_path()
        
        if not module_path:
            return discovered
        
        folder_path = module_path / folder_name
        
        if not folder_path.exists() or not folder_path.is_dir():
            return discovered
        
        # Importar el paquete de la carpeta
        package_name = f"{self.django_app}.{folder_name}"
        
        try:
            package = importlib.import_module(package_name)
        except ImportError:
            return discovered
        
        # Buscar archivos .py en la carpeta (excepto __init__.py)
        for py_file in folder_path.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            
            module_name = py_file.stem
            full_module_name = f"{package_name}.{module_name}"
            
            try:
                submodule = importlib.import_module(full_module_name)
                
                # Buscar clases en el módulo
                for name, obj in inspect.getmembers(submodule, inspect.isclass):
                    # Ignorar clases importadas de otros módulos
                    if obj.__module__ != full_module_name:
                        continue
                    
                    # Si hay una clase base, verificar herencia
                    if base_class and not issubclass(obj, base_class):
                        continue
                    
                    # Verificar por nombre de clase base (lazy)
                    if base_class_name:
                        base_names = [c.__name__ for c in obj.__mro__]
                        if base_class_name not in base_names:
                            continue
                    
                    discovered.append(obj)
                    
            except ImportError as e:
                # Log pero no fallar
                pass
        
        return discovered
    
    def get_models(self) -> List[Any]:
        """
        Retorna modelos descubiertos en la carpeta models/.
        
        Auto-descubre clases que heredan de:
        - AdemaBaseModel
        - django.db.models.Model
        """
        if self._discovered_models is not None:
            return self._discovered_models
        
        self._discovered_models = self._discover_in_folder(
            "models",
            base_class_name="Model"  # django.db.models.Model
        )
        
        return self._discovered_models
    
    def get_model_names(self) -> List[str]:
        """Retorna nombres de los modelos descubiertos."""
        return [m.__name__ for m in self.get_models()]
    
    def get_admin_classes(self) -> List[Any]:
        """
        Retorna clases Admin descubiertas en la carpeta admin/.
        
        Auto-descubre clases que heredan de ModelAdmin.
        """
        if self._discovered_admins is not None:
            return self._discovered_admins
        
        self._discovered_admins = self._discover_in_folder(
            "admin",
            base_class_name="ModelAdmin"
        )
        
        return self._discovered_admins
    
    def get_services(self) -> List[Any]:
        """
        Retorna servicios descubiertos en la carpeta services/.
        
        Auto-descubre clases que heredan de AdemaBaseService.
        """
        if self._discovered_services is not None:
            return self._discovered_services
        
        self._discovered_services = self._discover_in_folder(
            "services",
            base_class_name="AdemaBaseService"
        )
        
        # Si no hay servicios con AdemaBaseService, buscar cualquier clase Service
        if not self._discovered_services:
            all_classes = self._discover_in_folder("services")
            self._discovered_services = [
                c for c in all_classes 
                if c.__name__.endswith("Service")
            ]
        
        return self._discovered_services
    
    def get_urls(self) -> Optional[str]:
        """
        Retorna el path al módulo de URLs.
        
        Busca automáticamente {django_app}.urls
        """
        urls_module = f"{self.django_app}.urls"
        try:
            importlib.import_module(urls_module)
            return urls_module
        except ImportError:
            return None
    
    def get_templates_dir(self) -> Optional[str]:
        """Retorna el directorio de templates del módulo."""
        module_path = self._get_module_path()
        if module_path:
            templates_dir = module_path / "templates"
            if templates_dir.exists():
                return str(templates_dir)
        return None
    
    def get_static_dir(self) -> Optional[str]:
        """Retorna el directorio de archivos estáticos del módulo."""
        module_path = self._get_module_path()
        if module_path:
            static_dir = module_path / "static"
            if static_dir.exists():
                return str(static_dir)
        return None
    
    def get_fixtures(self) -> List[str]:
        """Retorna lista de fixtures que provee el módulo."""
        fixtures = []
        module_path = self._get_module_path()
        if module_path:
            fixtures_dir = module_path / "fixtures"
            if fixtures_dir.exists():
                for f in fixtures_dir.glob("*.json"):
                    fixtures.append(str(f))
                for f in fixtures_dir.glob("*.yaml"):
                    fixtures.append(str(f))
        return fixtures
    
    def get_migrations(self) -> Optional[str]:
        """Retorna el directorio de migraciones del módulo."""
        module_path = self._get_module_path()
        if module_path:
            migrations_dir = module_path / "migrations"
            if migrations_dir.exists():
                return str(migrations_dir)
        return None
    
    def get_settings(self) -> Dict[str, Any]:
        """
        Retorna configuraciones por defecto del módulo.
        Sobrescribir en subclases para definir settings.
        """
        return {}
    
    def on_install(self) -> None:
        """Hook ejecutado cuando el módulo se instala."""
        pass
    
    def on_uninstall(self) -> None:
        """Hook ejecutado cuando el módulo se desinstala."""
        pass
    
    def check_dependencies(self) -> List[str]:
        """Verifica que las dependencias del módulo estén instaladas."""
        missing = []
        for dep in self.metadata.dependencies:
            try:
                pkg_name = dep.split('>=')[0].split('==')[0].split('<')[0]
                pkg_name = pkg_name.replace('-', '_')
                __import__(pkg_name)
            except ImportError:
                missing.append(dep)
        return missing
    
    def get_entities_summary(self) -> Dict[str, List[str]]:
        """
        Retorna un resumen de todas las entidades del módulo.
        
        Returns:
            Dict con listas de nombres de models, admins, services
        """
        return {
            "models": self.get_model_names(),
            "admins": [a.__name__ for a in self.get_admin_classes()],
            "services": [s.__name__ for s in self.get_services()],
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el módulo a diccionario para API."""
        entities = self.get_entities_summary()
        return {
            **self.metadata.to_dict(),
            "models": entities["models"],
            "admins": entities["admins"],
            "services": entities["services"],
            "has_urls": self.get_urls() is not None,
            "has_templates": self.get_templates_dir() is not None,
            "has_static": self.get_static_dir() is not None,
        }


class BuiltinModule(AdemaModule):
    """
    Clase para módulos template que vienen incluidos con ADEMA core.
    
    Estos son módulos "template" que se generan cuando se crea
    un proyecto, no son paquetes Python externos instalados.
    """
    
    # Indica que es un template, no un paquete instalado
    is_template: bool = True
    
    def _get_module_path(self) -> Optional[Path]:
        """Los módulos builtin no tienen path real."""
        return None
    
    def get_models(self) -> List[Any]:
        """Los módulos template no tienen modelos reales."""
        return []
    
    def get_model_names(self) -> List[str]:
        """Retorna nombres sugeridos de modelos para este template."""
        # Sobrescribir en subclases para sugerir modelos
        return []
    
    def get_admin_classes(self) -> List[Any]:
        return []
    
    def get_services(self) -> List[Any]:
        return []
    
    def get_template_config(self) -> Dict[str, Any]:
        """
        Retorna la configuración para generar este módulo
        cuando se crea un nuevo proyecto.
        """
        return {
            "name": self.name,
            "label": self.label,
            "description": self.metadata.description,
            "suggested_models": self.get_model_names(),
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el módulo template."""
        return {
            **self.metadata.to_dict(),
            "is_template": True,
            "suggested_models": self.get_model_names(),
            "models": [],
            "admins": [],
            "services": [],
            "has_urls": False,
            "has_templates": False,
            "has_static": False,
        }

"""
ADEMA Module Registry
=====================

Registro central de módulos ADEMA.

El registro descubre automáticamente módulos instalados via:
1. Entry points de Python (paquetes instalados con pip)
2. Configuración manual en settings
3. Módulos built-in (templates)

El descubrimiento de módulos usa el sistema de entry_points de Python,
lo que permite que módulos externos como adema-ventas, adema-compras, etc.
se auto-registren al ser instalados con pip.

Entry point group: "adema.modules"

Ejemplo de pyproject.toml para un módulo externo:

    [project.entry-points."adema.modules"]
    ventas = "adema_ventas.module:VentasModule"
"""

import logging
from typing import Dict, List, Optional, Type, Any
from importlib.metadata import entry_points

from .base import AdemaModule, ModuleMetadata, BuiltinModule


logger = logging.getLogger(__name__)


class ModuleRegistry:
    """
    Registro singleton de módulos ADEMA.
    
    Mantiene un diccionario de todos los módulos disponibles,
    tanto instalados (paquetes pip) como templates (generados).
    
    Usage:
        from adema.modules import registry
        
        # Obtener todos los módulos
        modules = registry.get_all_modules()
        
        # Obtener un módulo específico
        ventas = registry.get_module("ventas")
        
        # Registrar un módulo custom
        registry.register_module(MyCustomModule)
    """
    
    _instance: Optional['ModuleRegistry'] = None
    
    def __new__(cls) -> 'ModuleRegistry':
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._modules: Dict[str, AdemaModule] = {}
            cls._instance._discovered = False
        return cls._instance
    
    def register_module(
        self, 
        module_class: Type[AdemaModule],
        override: bool = False
    ) -> bool:
        """
        Registra un módulo en el registro.
        
        Args:
            module_class: Clase del módulo a registrar
            override: Si True, sobrescribe si ya existe
            
        Returns:
            True si se registró exitosamente, False si ya existía
        """
        try:
            module = module_class()
            name = module.name
            
            if name in self._modules and not override:
                logger.warning(f"Módulo '{name}' ya está registrado, ignorando")
                return False
            
            self._modules[name] = module
            logger.info(f"Módulo '{name}' v{module.version} registrado")
            return True
            
        except Exception as e:
            logger.error(f"Error registrando módulo {module_class}: {e}")
            return False
    
    def unregister_module(self, name: str) -> bool:
        """
        Elimina un módulo del registro.
        
        Args:
            name: Nombre del módulo a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        if name in self._modules:
            del self._modules[name]
            logger.info(f"Módulo '{name}' eliminado del registro")
            return True
        return False
    
    def get_module(self, name: str) -> Optional[AdemaModule]:
        """
        Obtiene un módulo por su nombre.
        
        Args:
            name: Nombre del módulo
            
        Returns:
            Instancia del módulo o None si no existe
        """
        return self._modules.get(name)
    
    def get_all_modules(self) -> Dict[str, AdemaModule]:
        """
        Retorna todos los módulos registrados.
        
        Returns:
            Diccionario {nombre: módulo}
        """
        return self._modules.copy()
    
    def get_modules_list(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de módulos serializados para API.
        
        Returns:
            Lista de diccionarios con info de módulos
        """
        return [module.to_dict() for module in self._modules.values()]
    
    def get_modules_by_category(self, category: str) -> List[AdemaModule]:
        """
        Filtra módulos por categoría.
        
        Args:
            category: Categoría a filtrar (erp, crm, utils, etc.)
            
        Returns:
            Lista de módulos en esa categoría
        """
        return [
            module for module in self._modules.values()
            if module.metadata.category == category
        ]
    
    def get_installed_modules(self) -> List[AdemaModule]:
        """
        Retorna solo módulos que son paquetes instalados.
        
        Returns:
            Lista de módulos instalados (no templates)
        """
        return [
            module for module in self._modules.values()
            if not isinstance(module, BuiltinModule)
        ]
    
    def get_template_modules(self) -> List[AdemaModule]:
        """
        Retorna solo módulos template (built-in).
        
        Returns:
            Lista de módulos template
        """
        return [
            module for module in self._modules.values()
            if isinstance(module, BuiltinModule)
        ]
    
    def is_registered(self, name: str) -> bool:
        """Verifica si un módulo está registrado."""
        return name in self._modules
    
    def clear(self) -> None:
        """Limpia todos los módulos del registro."""
        self._modules.clear()
        self._discovered = False
    
    @property
    def count(self) -> int:
        """Número de módulos registrados."""
        return len(self._modules)


# Instancia singleton global
registry = ModuleRegistry()


def discover_modules(force: bool = False) -> int:
    """
    Descubre y registra módulos automáticamente.
    
    Busca módulos en:
    1. Entry points "adema.modules" (paquetes instalados)
    2. Módulos built-in de ADEMA
    
    Args:
        force: Si True, re-descubre aunque ya se haya hecho
        
    Returns:
        Número de módulos descubiertos
    """
    global registry
    
    if registry._discovered and not force:
        return registry.count
    
    count_before = registry.count
    
    # 1. Registrar módulos built-in (templates)
    _register_builtin_modules()
    
    # 2. Descubrir módulos via entry_points
    _discover_entry_points()
    
    registry._discovered = True
    
    discovered = registry.count - count_before
    logger.info(f"Descubiertos {discovered} módulos, total: {registry.count}")
    
    return discovered


def _register_builtin_modules() -> None:
    """Registra los módulos template que vienen con ADEMA."""
    
    # Módulos template disponibles para generar en nuevos proyectos
    # Estos NO son paquetes instalados, son templates de código
    
    class VentasTemplate(BuiltinModule):
        metadata = ModuleMetadata(
            name="ventas",
            label="Ventas",
            description="Módulo de gestión de ventas y pedidos",
            icon="🛒",
            category="erp",
            tags=["ventas", "pedidos", "clientes", "facturación"],
        )
        
        def get_model_names(self) -> List[str]:
            """Modelos sugeridos para el módulo de ventas."""
            return ["Venta", "LineaVenta", "Cotizacion", "LineaCotizacion"]
    
    class ComprasTemplate(BuiltinModule):
        metadata = ModuleMetadata(
            name="compras",
            label="Compras",
            description="Módulo de gestión de compras y proveedores",
            icon="📦",
            category="erp",
            tags=["compras", "proveedores", "órdenes"],
        )
        
        def get_model_names(self) -> List[str]:
            return ["OrdenCompra", "LineaCompra", "Proveedor"]
    
    class InventarioTemplate(BuiltinModule):
        metadata = ModuleMetadata(
            name="inventario",
            label="Inventario",
            description="Gestión de stock, productos y movimientos",
            icon="📊",
            category="erp",
            tags=["stock", "productos", "almacén", "movimientos"],
        )
        
        def get_model_names(self) -> List[str]:
            return ["Producto", "Categoria", "Almacen", "MovimientoStock"]
    
    class ClientesTemplate(BuiltinModule):
        metadata = ModuleMetadata(
            name="clientes",
            label="Clientes (CRM)",
            description="Gestión de clientes, contactos y seguimiento",
            icon="👥",
            category="crm",
            tags=["clientes", "contactos", "crm", "seguimiento"],
        )
        
        def get_model_names(self) -> List[str]:
            return ["Cliente", "Contacto", "Interaccion", "Oportunidad"]
    
    class FacturacionTemplate(BuiltinModule):
        metadata = ModuleMetadata(
            name="facturacion",
            label="Facturación",
            description="Emisión y control de facturas y comprobantes",
            icon="📄",
            category="erp",
            tags=["facturas", "comprobantes", "afip", "fiscal"],
        )
        
        def get_model_names(self) -> List[str]:
            return ["Factura", "LineaFactura", "NotaCredito", "Recibo"]
    
    class ReportesTemplate(BuiltinModule):
        metadata = ModuleMetadata(
            name="reportes",
            label="Reportes",
            description="Dashboard y reportes analíticos",
            icon="📈",
            category="utils",
            tags=["reportes", "dashboard", "analytics", "kpi"],
        )
        
        def get_model_names(self) -> List[str]:
            return ["Reporte", "Dashboard", "Widget", "KPI"]
    
    # Registrar todos los templates
    templates = [
        VentasTemplate,
        ComprasTemplate,
        InventarioTemplate,
        ClientesTemplate,
        FacturacionTemplate,
        ReportesTemplate,
    ]
    
    for template_class in templates:
        registry.register_module(template_class)


def _discover_entry_points() -> None:
    """
    Descubre módulos instalados via entry_points.
    
    Los módulos externos (adema-ventas, adema-compras, etc.) se registran
    automáticamente si definen un entry_point en el grupo "adema.modules".
    """
    try:
        # Python 3.10+ usa groups como diccionario
        eps = entry_points()
        
        if hasattr(eps, 'select'):
            # Python 3.10+
            adema_eps = eps.select(group='adema.modules')
        elif hasattr(eps, 'get'):
            # Python 3.9
            adema_eps = eps.get('adema.modules', [])
        else:
            # Fallback para versiones más antiguas
            adema_eps = []
        
        for ep in adema_eps:
            try:
                module_class = ep.load()
                if issubclass(module_class, AdemaModule):
                    # Override built-in si hay un paquete instalado
                    registry.register_module(module_class, override=True)
                    logger.info(f"Módulo externo cargado: {ep.name}")
            except Exception as e:
                logger.warning(f"Error cargando módulo {ep.name}: {e}")
                
    except Exception as e:
        logger.error(f"Error descubriendo entry_points: {e}")


def get_module_for_django_app(django_app: str) -> Optional[AdemaModule]:
    """
    Busca un módulo por su nombre de app Django.
    
    Args:
        django_app: Nombre de la app Django (ej: "adema_ventas")
        
    Returns:
        El módulo correspondiente o None
    """
    for module in registry.get_all_modules().values():
        if module.django_app == django_app:
            return module
    return None


def check_module_dependencies(module_name: str) -> Dict[str, Any]:
    """
    Verifica las dependencias de un módulo.
    
    Args:
        module_name: Nombre del módulo a verificar
        
    Returns:
        Diccionario con estado de dependencias
    """
    module = registry.get_module(module_name)
    if not module:
        return {"error": f"Módulo '{module_name}' no encontrado"}
    
    missing = module.check_dependencies()
    
    return {
        "module": module_name,
        "dependencies": module.metadata.dependencies,
        "missing": missing,
        "all_satisfied": len(missing) == 0,
    }

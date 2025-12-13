"""
ADEMA Module Configuration
==========================

Configuración centralizada para el sistema de módulos.

Este archivo permite:
1. Configurar qué módulos están habilitados por defecto
2. Definir categorías de módulos
3. Configurar el comportamiento del descubrimiento automático

Uso en settings.py de un proyecto Django:

    ADEMA_MODULES = {
        'auto_discover': True,
        'enabled_modules': ['ventas', 'inventario'],
        'disabled_modules': [],
    }
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ModuleCategory:
    """Definición de una categoría de módulos."""
    name: str
    label: str
    description: str = ""
    icon: str = "📁"
    order: int = 0


# Categorías predefinidas de módulos
DEFAULT_CATEGORIES: Dict[str, ModuleCategory] = {
    "erp": ModuleCategory(
        name="erp",
        label="ERP / Gestión Empresarial",
        description="Módulos para gestión empresarial, ventas, compras, inventario",
        icon="🏢",
        order=1,
    ),
    "crm": ModuleCategory(
        name="crm",
        label="CRM / Clientes",
        description="Módulos para gestión de clientes y relaciones comerciales",
        icon="👥",
        order=2,
    ),
    "finance": ModuleCategory(
        name="finance",
        label="Finanzas / Contabilidad",
        description="Módulos financieros y contables",
        icon="💰",
        order=3,
    ),
    "hr": ModuleCategory(
        name="hr",
        label="Recursos Humanos",
        description="Módulos para gestión de personal",
        icon="👔",
        order=4,
    ),
    "utils": ModuleCategory(
        name="utils",
        label="Utilidades",
        description="Módulos de utilidad general, reportes, dashboards",
        icon="🔧",
        order=5,
    ),
    "general": ModuleCategory(
        name="general",
        label="General",
        description="Otros módulos",
        icon="📦",
        order=99,
    ),
}


@dataclass 
class AdemModulesConfig:
    """
    Configuración del sistema de módulos ADEMA.
    
    Attributes:
        auto_discover: Si True, descubre módulos automáticamente al iniciar
        enabled_modules: Lista de módulos habilitados (si vacía, todos están habilitados)
        disabled_modules: Lista de módulos explícitamente deshabilitados
        module_paths: Paths adicionales donde buscar módulos
        categories: Categorías de módulos
    """
    auto_discover: bool = True
    enabled_modules: List[str] = field(default_factory=list)
    disabled_modules: List[str] = field(default_factory=list)
    module_paths: List[str] = field(default_factory=list)
    categories: Dict[str, ModuleCategory] = field(default_factory=lambda: DEFAULT_CATEGORIES.copy())
    
    def is_module_enabled(self, module_name: str) -> bool:
        """
        Verifica si un módulo está habilitado.
        
        Args:
            module_name: Nombre del módulo
            
        Returns:
            True si el módulo está habilitado
        """
        # Si está explícitamente deshabilitado
        if module_name in self.disabled_modules:
            return False
        
        # Si hay lista de habilitados, debe estar en ella
        if self.enabled_modules:
            return module_name in self.enabled_modules
        
        # Por defecto, todos están habilitados
        return True
    
    def get_category(self, category_name: str) -> Optional[ModuleCategory]:
        """Obtiene una categoría por nombre."""
        return self.categories.get(category_name)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa la configuración a diccionario."""
        return {
            "auto_discover": self.auto_discover,
            "enabled_modules": self.enabled_modules,
            "disabled_modules": self.disabled_modules,
            "module_paths": self.module_paths,
            "categories": {
                name: {
                    "name": cat.name,
                    "label": cat.label,
                    "description": cat.description,
                    "icon": cat.icon,
                }
                for name, cat in self.categories.items()
            },
        }


# Configuración por defecto
_default_config = AdemModulesConfig()


def get_config() -> AdemModulesConfig:
    """
    Obtiene la configuración actual de módulos.
    
    Intenta cargar desde Django settings si está disponible,
    sino retorna la configuración por defecto.
    
    Returns:
        Configuración de módulos
    """
    try:
        from django.conf import settings
        
        if hasattr(settings, 'ADEMA_MODULES'):
            config_dict = settings.ADEMA_MODULES
            return AdemModulesConfig(
                auto_discover=config_dict.get('auto_discover', True),
                enabled_modules=config_dict.get('enabled_modules', []),
                disabled_modules=config_dict.get('disabled_modules', []),
                module_paths=config_dict.get('module_paths', []),
            )
    except Exception:
        pass
    
    return _default_config


def set_config(config: AdemModulesConfig) -> None:
    """
    Establece la configuración de módulos.
    
    Args:
        config: Nueva configuración
    """
    global _default_config
    _default_config = config

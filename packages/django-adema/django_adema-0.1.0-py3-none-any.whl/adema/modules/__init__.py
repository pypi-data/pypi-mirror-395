"""
ADEMA Modules System
====================

Sistema de plugins modulares para ADEMA Framework.

Este módulo provee:
- Registro dinámico de módulos externos (adema-ventas, adema-compras, etc.)
- Descubrimiento automático de módulos instalados via entry_points
- Auto-descubrimiento de entidades en carpetas (models/, admin/, services/)
- Clases base para crear nuevos módulos

Estructura de un módulo externo:
    adema_ventas/
    ├── module.py           # Clase VentasModule (solo metadata)
    ├── models/             # Un archivo por entidad
    │   ├── venta.py
    │   └── linea_venta.py
    ├── admin/              # Un archivo por admin
    │   └── venta_admin.py
    └── services/           # Un archivo por servicio
        └── venta_service.py

Uso:
    from adema.modules import registry, discover_modules
    
    # Descubrir módulos instalados
    discover_modules()
    
    # Obtener módulos disponibles
    modules = registry.get_all_modules()
    
    # El módulo auto-descubre entidades en las carpetas
    ventas = registry.get_module('ventas')
    print(ventas.get_model_names())  # ['Venta', 'LineaVenta', ...]
"""

from .base import AdemaModule, ModuleMetadata, BuiltinModule
from .registry import ModuleRegistry, registry, discover_modules

__all__ = [
    'AdemaModule',
    'ModuleMetadata',
    'BuiltinModule',
    'ModuleRegistry',
    'registry',
    'discover_modules',
]

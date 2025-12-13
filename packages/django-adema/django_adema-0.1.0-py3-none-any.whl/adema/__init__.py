"""
ADEMA Framework - Django Project Generator
==========================================

A meta-framework and CLI tool for generating Django projects 
with a "Vertical Slicing" architecture optimized for ERP/CRM applications.

Example:
    >>> import adema
    >>> print(adema.__version__)
    '0.1.0'

Note:
    The base components (AdemaBaseModel, AdemaBaseService, AdemaAppConfig)
    require Django to be configured. They are available via lazy imports
    to allow the CLI tools to work without Django installed.
    
    To use base components in a Django project:
        from adema.base.models import AdemaBaseModel
        from adema.base.services import AdemaBaseService
        from adema.base.apps import AdemaAppConfig
    
    For the module system:
        from adema.modules import registry, discover_modules, AdemaModule
"""

__version__ = '0.1.0'
__author__ = 'ADEMA Team'
__license__ = 'MIT'

__all__ = [
    '__version__',
    'AdemaBaseModel',
    'AdemaBaseService', 
    'AdemaAppConfig',
    # Module system
    'AdemaModule',
    'ModuleMetadata',
    'registry',
    'discover_modules',
]


def __getattr__(name):
    """
    Lazy import of Django-dependent components.
    
    This allows the CLI to work without Django being configured,
    while still exposing the base components when they're actually needed.
    """
    if name == 'AdemaBaseModel':
        from adema.base.models import AdemaBaseModel
        return AdemaBaseModel
    elif name == 'AdemaBaseService':
        from adema.base.services import AdemaBaseService
        return AdemaBaseService
    elif name == 'AdemaAppConfig':
        from adema.base.apps import AdemaAppConfig
        return AdemaAppConfig
    # Module system lazy imports
    elif name == 'AdemaModule':
        from adema.modules.base import AdemaModule
        return AdemaModule
    elif name == 'ModuleMetadata':
        from adema.modules.base import ModuleMetadata
        return ModuleMetadata
    elif name == 'registry':
        from adema.modules.registry import registry
        return registry
    elif name == 'discover_modules':
        from adema.modules.registry import discover_modules
        return discover_modules
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

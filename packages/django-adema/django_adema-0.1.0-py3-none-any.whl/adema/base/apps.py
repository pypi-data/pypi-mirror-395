"""
ADEMA App Configuration
=======================

Custom AppConfig with auto-discovery features for ADEMA apps.
Automatically discovers and registers signals, admin, and URLs.

Usage:
    # In your app's apps.py:
    from adema.base.apps import AdemaAppConfig
    
    class VentasConfig(AdemaAppConfig):
        name = 'apps.ventas'
        verbose_name = 'Ventas'
"""

import importlib
import logging
from django.apps import AppConfig


logger = logging.getLogger(__name__)


class AdemaAppConfig(AppConfig):
    """
    Enhanced AppConfig for ADEMA apps with auto-discovery.
    
    Features:
        - Auto-discovers and imports signals module
        - Auto-discovers and imports admin module  
        - Provides hooks for custom initialization
    
    Example:
        class InventarioConfig(AdemaAppConfig):
            name = 'apps.inventario'
            verbose_name = 'Inventario'
            
            # Optional: Override auto-discovery
            auto_discover_signals = True
            auto_discover_admin = True
            
            def ready(self):
                super().ready()
                # Custom initialization
                self.setup_cache()
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Auto-discovery flags
    auto_discover_signals = True
    auto_discover_admin = True
    auto_discover_tasks = True  # For Celery tasks
    
    def ready(self):
        """
        Called when the app is ready.
        Performs auto-discovery of signals, admin, and tasks.
        """
        self._discover_signals()
        self._discover_admin()
        self._discover_tasks()
        
        # Log that the app is ready
        logger.debug(f"App '{self.name}' is ready")
    
    def _discover_signals(self):
        """Auto-discover and import signals module."""
        if not self.auto_discover_signals:
            return
        
        try:
            signals_module = f'{self.name}.signals'
            importlib.import_module(signals_module)
            logger.debug(f"Discovered signals in {signals_module}")
        except ImportError:
            # No signals module - that's fine
            pass
        except Exception as e:
            logger.warning(f"Error importing signals for {self.name}: {e}")
    
    def _discover_admin(self):
        """Auto-discover and import admin configurations."""
        if not self.auto_discover_admin:
            return
        
        # Try importing from admin/ directory
        admin_modules = [
            f'{self.name}.admin',
            f'{self.name}.admin.dashboard',
            f'{self.name}.admin.inlines',
        ]
        
        for module in admin_modules:
            try:
                importlib.import_module(module)
                logger.debug(f"Discovered admin in {module}")
            except ImportError:
                pass
            except Exception as e:
                logger.warning(f"Error importing admin {module}: {e}")
    
    def _discover_tasks(self):
        """Auto-discover and import Celery tasks."""
        if not self.auto_discover_tasks:
            return
        
        try:
            tasks_module = f'{self.name}.tasks'
            importlib.import_module(tasks_module)
            logger.debug(f"Discovered tasks in {tasks_module}")
        except ImportError:
            # No tasks module - that's fine
            pass
        except Exception as e:
            logger.warning(f"Error importing tasks for {self.name}: {e}")
    
    @classmethod
    def get_models(cls):
        """
        Get all models from this app.
        
        Returns:
            List of model classes
        """
        from django.apps import apps
        return list(apps.get_app_config(cls.label).get_models())
    
    @classmethod  
    def get_model(cls, model_name):
        """
        Get a specific model by name.
        
        Args:
            model_name: Name of the model (case-insensitive)
            
        Returns:
            Model class or None
        """
        from django.apps import apps
        try:
            return apps.get_model(cls.label, model_name)
        except LookupError:
            return None

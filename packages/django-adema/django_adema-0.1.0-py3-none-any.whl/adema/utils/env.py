"""
ADEMA Environment Configuration
===============================

Safe wrapper around django-environ for type-safe configuration.
Provides convenient functions for reading environment variables
with proper defaults and type conversion.

Usage:
    from adema.utils.env import env, get_env, require_env
    
    # Get with default
    DEBUG = get_env('DEBUG', default=False, cast=bool)
    
    # Require (raises if not set)
    SECRET_KEY = require_env('SECRET_KEY')
    
    # Using the env object directly
    DATABASE_URL = env.db('DATABASE_URL')
"""

import os
from pathlib import Path
from typing import Any, Callable, List, Optional, Type, TypeVar, Union

try:
    import environ
    ENVIRON_AVAILABLE = True
except ImportError:
    ENVIRON_AVAILABLE = False


T = TypeVar('T')


class EnvWrapper:
    """
    Wrapper around django-environ with additional safety features.
    
    Provides:
        - Type-safe environment variable access
        - Default values
        - Required variable validation
        - Common type conversions
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize the environment wrapper.
        
        Args:
            env_file: Path to .env file. If None, will try to find it.
        """
        if ENVIRON_AVAILABLE:
            self._env = environ.Env()
            
            # Try to read .env file
            if env_file:
                env_path = Path(env_file)
            else:
                # Search for .env file in common locations
                env_path = self._find_env_file()
            
            if env_path and env_path.exists():
                environ.Env.read_env(str(env_path))
        else:
            self._env = None
    
    def _find_env_file(self) -> Optional[Path]:
        """Find .env file in common locations."""
        # Try current directory and parents
        current = Path.cwd()
        
        for _ in range(5):  # Search up to 5 levels
            env_path = current / '.env'
            if env_path.exists():
                return env_path
            
            parent = current.parent
            if parent == current:
                break
            current = parent
        
        return None
    
    def __call__(
        self,
        var: str,
        default: Any = None,
        cast: Optional[Callable] = None
    ) -> Any:
        """
        Get an environment variable with optional casting.
        
        Args:
            var: Environment variable name
            default: Default value if not set
            cast: Function to cast the value (e.g., int, bool, list)
            
        Returns:
            The environment variable value, cast if specified
        """
        if self._env:
            try:
                if cast:
                    return self._env(var, default=default, cast=cast)
                return self._env(var, default=default)
            except Exception:
                return default
        
        # Fallback to os.environ
        value = os.environ.get(var, default)
        if value is not None and cast:
            return cast(value)
        return value
    
    def str(self, var: str, default: str = '') -> str:
        """Get a string environment variable."""
        return self(var, default=default, cast=str)
    
    def int(self, var: str, default: int = 0) -> int:
        """Get an integer environment variable."""
        return self(var, default=default, cast=int)
    
    def float(self, var: str, default: float = 0.0) -> float:
        """Get a float environment variable."""
        return self(var, default=default, cast=float)
    
    def bool(self, var: str, default: bool = False) -> bool:
        """
        Get a boolean environment variable.
        
        Recognizes: true, yes, 1, on (case-insensitive) as True
        """
        if self._env:
            return self(var, default=default, cast=bool)
        
        value = os.environ.get(var)
        if value is None:
            return default
        
        return value.lower() in ('true', 'yes', '1', 'on')
    
    def list(
        self,
        var: str,
        default: Optional[List] = None,
        separator: str = ','
    ) -> List[str]:
        """
        Get a list environment variable.
        
        Args:
            var: Environment variable name
            default: Default list if not set
            separator: Character to split on (default: comma)
            
        Returns:
            List of strings
        """
        if self._env:
            try:
                return self._env.list(var, default=default or [])
            except Exception:
                return default or []
        
        value = os.environ.get(var)
        if value is None:
            return default or []
        
        return [item.strip() for item in value.split(separator)]
    
    def db(
        self,
        var: str = 'DATABASE_URL',
        default: Optional[str] = None
    ) -> dict:
        """
        Get database configuration from URL.
        
        Supports:
            - postgres://user:pass@host:port/dbname
            - sqlite:///path/to/db.sqlite3
            - mysql://user:pass@host:port/dbname
        
        Args:
            var: Environment variable name (default: DATABASE_URL)
            default: Default database URL
            
        Returns:
            Django DATABASES configuration dict
        """
        if self._env:
            try:
                return self._env.db(var, default=default)
            except Exception:
                pass
        
        # Fallback parsing
        url = os.environ.get(var, default)
        if not url:
            return {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        
        return self._parse_db_url(url)
    
    def _parse_db_url(self, url: str) -> dict:
        """Parse a database URL into Django config."""
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        
        engines = {
            'postgres': 'django.db.backends.postgresql',
            'postgresql': 'django.db.backends.postgresql',
            'mysql': 'django.db.backends.mysql',
            'sqlite': 'django.db.backends.sqlite3',
        }
        
        engine = engines.get(parsed.scheme, 'django.db.backends.sqlite3')
        
        if parsed.scheme == 'sqlite':
            return {
                'ENGINE': engine,
                'NAME': parsed.path.lstrip('/') or 'db.sqlite3',
            }
        
        return {
            'ENGINE': engine,
            'NAME': parsed.path.lstrip('/'),
            'USER': parsed.username or '',
            'PASSWORD': parsed.password or '',
            'HOST': parsed.hostname or 'localhost',
            'PORT': str(parsed.port or ''),
        }
    
    def cache(
        self,
        var: str = 'CACHE_URL',
        default: Optional[str] = None
    ) -> dict:
        """
        Get cache configuration from URL.
        
        Args:
            var: Environment variable name
            default: Default cache URL
            
        Returns:
            Django CACHES configuration dict
        """
        if self._env:
            try:
                return self._env.cache(var, default=default)
            except Exception:
                pass
        
        # Default to local memory cache
        return {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    
    def email(
        self,
        var: str = 'EMAIL_URL',
        default: Optional[str] = None
    ) -> dict:
        """
        Get email configuration from URL.
        
        Args:
            var: Environment variable name
            default: Default email URL
            
        Returns:
            Django email configuration dict
        """
        if self._env:
            try:
                return self._env.email(var, default=default)
            except Exception:
                pass
        
        # Default to console backend
        return {
            'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',
        }
    
    def path(self, var: str, default: Optional[str] = None) -> Path:
        """
        Get a path environment variable.
        
        Args:
            var: Environment variable name
            default: Default path
            
        Returns:
            Path object
        """
        value = self(var, default=default)
        return Path(value) if value else Path(default or '.')


# Global instance
env = EnvWrapper()


def get_env(
    var: str,
    default: Any = None,
    cast: Optional[Callable[[str], T]] = None
) -> Union[T, Any]:
    """
    Get an environment variable with optional type casting.
    
    Args:
        var: Environment variable name
        default: Default value if not set
        cast: Function to cast the value
        
    Returns:
        The environment variable value
        
    Example:
        DEBUG = get_env('DEBUG', default=False, cast=bool)
        PORT = get_env('PORT', default=8000, cast=int)
    """
    return env(var, default=default, cast=cast)


def require_env(var: str, cast: Optional[Callable] = None) -> Any:
    """
    Get a required environment variable.
    
    Raises:
        ValueError: If the environment variable is not set
        
    Args:
        var: Environment variable name
        cast: Optional function to cast the value
        
    Returns:
        The environment variable value
        
    Example:
        SECRET_KEY = require_env('SECRET_KEY')
    """
    value = os.environ.get(var)
    
    if value is None:
        raise ValueError(
            f"Required environment variable '{var}' is not set. "
            f"Please set it in your .env file or environment."
        )
    
    if cast:
        return cast(value)
    return value

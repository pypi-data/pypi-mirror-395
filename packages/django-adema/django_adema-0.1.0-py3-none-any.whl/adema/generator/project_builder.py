"""
ADEMA Project Builder
=====================

Handles the generation of complete ADEMA Django projects using Jinja2 templates.
This is the core engine that creates projects from the Web Wizard configuration.
"""

import os
import shutil
import secrets
from pathlib import Path
from typing import Dict, Any, List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape


class ProjectBuilder:
    """
    Builds a complete ADEMA Django project from configuration.
    
    This class handles:
    - Creating the project directory structure
    - Rendering Jinja2 templates with configuration values
    - Copying static template files
    - Post-processing generated files
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the project builder.
        
        Args:
            config: Project configuration dictionary containing:
                - name: Project name
                - database: Database configuration
                - modules: List of modules to include
                - output_dir: Where to create the project
        """
        self.config = config
        self.project_name = config.get('name', 'my_project')
        self.output_dir = Path(config.get('output_dir', '.')).resolve()
        self.project_dir = self.output_dir / self.project_name
        
        # Setup Jinja2 environment
        self.template_dir = self._get_template_dir()
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            keep_trailing_newline=True,
        )
        
        # Generate a secret key for Django
        self.secret_key = secrets.token_urlsafe(50)
    
    def _write_file(self, path: Path, content: str) -> None:
        """
        Write content to file with UTF-8 encoding.
        
        This ensures proper handling of special characters on Windows.
        """
        path.write_text(content, encoding='utf-8')
    
    def _get_template_dir(self) -> Path:
        """Get the path to the project template directory."""
        from importlib import resources
        
        try:
            template_files = resources.files('adema.templates')
            with resources.as_file(template_files / 'project_template') as path:
                return Path(path)
        except Exception:
            # Fallback to __file__ based resolution
            return Path(__file__).parent.parent / 'templates' / 'project_template'
    
    def build(self) -> str:
        """
        Build the complete project.
        
        Returns:
            Path to the created project directory.
        """
        # Validate
        if self.project_dir.exists():
            raise ValueError(f"Directory already exists: {self.project_dir}")
        
        # Create project structure
        self._create_directory_structure()
        
        # Generate configuration files
        self._generate_config_files()
        
        # Generate settings
        self._generate_settings()
        
        # Generate manage.py
        self._generate_manage_py()
        
        # Generate URL configuration
        self._generate_urls()
        
        # Generate WSGI/ASGI
        self._generate_wsgi_asgi()
        
        # Copy static files
        self._copy_static_files()
        
        # Generate home template
        self._generate_home_template()
        
        # Generate modules if specified
        if self.config.get('modules'):
            self._generate_modules()
        
        return str(self.project_dir)
    
    def _create_directory_structure(self):
        """Create the base directory structure."""
        directories = [
            self.project_dir,
            self.project_dir / 'config',
            self.project_dir / 'config' / 'settings',
            self.project_dir / 'apps',
            self.project_dir / 'static',
            self.project_dir / 'media',
            self.project_dir / 'templates',
            self.project_dir / 'locale',
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _generate_config_files(self):
        """Generate root configuration files."""
        # .env.example
        env_content = self._render_env_example()
        self._write_file(self.project_dir / '.env.example', env_content)
        self._write_file(self.project_dir / '.env', env_content)
        
        # .gitignore
        gitignore_content = self._render_gitignore()
        self._write_file(self.project_dir / '.gitignore', gitignore_content)
        
        # requirements.txt
        requirements_content = self._render_requirements()
        self._write_file(self.project_dir / 'requirements.txt', requirements_content)
        
        # README.md
        readme_content = self._render_readme()
        self._write_file(self.project_dir / 'README.md', readme_content)
        
        # config/__init__.py
        self._write_file(self.project_dir / 'config' / '__init__.py', '')
        
        # config/settings/__init__.py
        self._write_file(self.project_dir / 'config' / 'settings' / '__init__.py', '')
        
        # apps/__init__.py
        self._write_file(self.project_dir / 'apps' / '__init__.py', '')
    
    def _generate_settings(self):
        """Generate Django settings files."""
        settings_dir = self.project_dir / 'config' / 'settings'
        
        # base.py
        base_settings = self._render_base_settings()
        self._write_file(settings_dir / 'base.py', base_settings)
        
        # local.py
        local_settings = self._render_local_settings()
        self._write_file(settings_dir / 'local.py', local_settings)
        
        # production.py
        production_settings = self._render_production_settings()
        self._write_file(settings_dir / 'production.py', production_settings)
    
    def _generate_manage_py(self):
        """Generate manage.py."""
        content = f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''
        self._write_file(self.project_dir / 'manage.py', content)
    
    def _generate_urls(self):
        """Generate URL configuration."""
        
        # Build module URLs
        module_urls = []
        modules = self.config.get('modules', [])
        for module in modules:
            if isinstance(module, dict):
                name = module.get('name')
            else:
                name = module
            
            if name:
                module_urls.append(f"    path('{name}/', include('apps.{name}.urls')),")
        
        module_urls_str = '\n'.join(module_urls)

        content = f'''"""
URL Configuration for {self.project_name}
==========================================

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # Module URLs
{module_urls_str}
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
        self._write_file(self.project_dir / 'config' / 'urls.py', content)
    
    def _generate_wsgi_asgi(self):
        """Generate WSGI and ASGI configuration."""
        # wsgi.py
        wsgi_content = f'''"""
WSGI config for {self.project_name} project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
'''
        self._write_file(self.project_dir / 'config' / 'wsgi.py', wsgi_content)
        
        # asgi.py
        asgi_content = f'''"""
ASGI config for {self.project_name} project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_asgi_application()
'''
        self._write_file(self.project_dir / 'config' / 'asgi.py', asgi_content)
    
    def _copy_static_files(self):
        """Copy static template files."""
        # Create base template
        templates_dir = self.project_dir / 'templates'
        base_html = '''{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}''' + self.project_name + '''{% endblock %}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">''' + self.project_name.replace('_', ' ').title() + '''</a>
        </div>
    </nav>
    
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''
        self._write_file(templates_dir / 'base.html', base_html)
    
    def _generate_home_template(self):
        """Generate the home page template."""
        modules = self.config.get('modules', [])
        module_links = []
        for module in modules:
            if isinstance(module, dict):
                name = module.get('name')
                label = module.get('label', name.title())
            else:
                name = module
                label = name.title()
            
            if name:
                module_links.append(f'''
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-body text-center">
                    <h5 class="card-title">{label}</h5>
                    <p class="card-text">Gestionar {label.lower()}.</p>
                    <a href="/{name}/" class="btn btn-primary">Ir a {label}</a>
                </div>
            </div>
        </div>''')
        
        links_html = '\\n'.join(module_links)
        
        content = f'''{{% extends "base.html" %}}

{{% block content %}}
<div class="container mt-5">
    <div class="jumbotron text-center mb-5">
        <h1 class="display-4">Bienvenido a {self.project_name.replace('_', ' ').title()}</h1>
        <p class="lead">{self.config.get('description', 'Sistema generado con ADEMA Framework')}</p>
        <hr class="my-4">
        <p>Seleccione un módulo para comenzar:</p>
    </div>

    <div class="row">
{links_html}
        
        <div class="col-md-4 mb-4">
            <div class="card h-100 border-secondary">
                <div class="card-body text-center">
                    <h5 class="card-title">Admin</h5>
                    <p class="card-text">Panel de administración de Django.</p>
                    <a href="/admin/" class="btn btn-secondary">Ir al Admin</a>
                </div>
            </div>
        </div>
    </div>
</div>
{{% endblock %}}
'''
        self._write_file(self.project_dir / 'templates' / 'index.html', content)

    def _generate_modules(self):
        """Generate app modules specified in configuration."""
        modules = self.config.get('modules', [])
        
        for module in modules:
            if isinstance(module, dict):
                module_name = module.get('name')
            else:
                module_name = module
            
            if module_name:
                app_builder = AppBuilder({
                    'name': module_name,
                    'output_dir': str(self.project_dir / 'apps'),
                })
                app_builder.build()
    
    def _render_env_example(self) -> str:
        """Render .env.example file."""
        db_config = self.config.get('database', {})
        
        # Handle both string and dict formats for backwards compatibility
        if isinstance(db_config, str):
            db_engine = db_config
            db_config = {'engine': db_config}
        else:
            db_engine = db_config.get('engine', 'sqlite')
        
        content = f'''# Django Settings
DEBUG=True
SECRET_KEY={self.secret_key}
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
'''
        
        if db_engine == 'postgres':
            db_name = db_config.get('name', self.project_name)
            db_host = db_config.get('host', 'localhost')
            db_port = db_config.get('port', 5432)
            db_user = db_config.get('user', 'postgres')
            content += f'''DATABASE_URL=postgres://{db_user}:your_password@{db_host}:{db_port}/{db_name}
'''
        else:
            content += '''DATABASE_URL=sqlite:///db.sqlite3
'''
        
        content += '''
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
'''

        if self.config.get('include_ai', False):
            content += '''
# AI Configuration (Local / Cloud)
AI_PROVIDER=ollama
AI_MODEL=llama3
AI_BASE_URL=http://localhost:11434
AI_API_KEY=
# To use OpenAI, set provider to 'openai' and add your key
'''

        content += '''
# Security (Production)
CSRF_TRUSTED_ORIGINS=
SECURE_SSL_REDIRECT=False
'''
        return content
    
    def _render_gitignore(self) -> str:
        """Render .gitignore file."""
        return '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/

# Distribution
dist/
build/
*.egg-info/
'''
    
    def _render_requirements(self) -> str:
        """Render requirements.txt file."""
        requirements = [
            '# Core Django',
            'Django>=4.2',
            'python-dotenv>=1.0.0',
            '',
            '# Database',
        ]
        
        db_config = self.config.get('database', {})
        # Handle both string and dict formats for backwards compatibility
        if isinstance(db_config, str):
            db_engine = db_config
        else:
            db_engine = db_config.get('engine', 'sqlite')
        
        if db_engine == 'postgres':
            requirements.append('psycopg2-binary>=2.9.9')
        
        requirements.extend([
            '',
            '# ADEMA Framework',
        ])
        
        if self.config.get('include_ai'):
            requirements.append('django-adema[ai]>=0.1.0')
        else:
            requirements.append('django-adema>=0.1.0')
            
        requirements.extend([
            '',
            '# Production Server',
            'gunicorn>=21.0.0',
            'whitenoise>=6.6.0',
        ])
        
        if self.config.get('use_rest_api'):
            requirements.extend([
                '',
                '# REST API',
                'djangorestframework>=3.14.0',
                'django-cors-headers>=4.3.0',
                'drf-spectacular>=0.26.0',
            ])
        
        if self.config.get('use_celery'):
            requirements.extend([
                '',
                '# Async Tasks (Celery)',
                'celery>=5.3.0',
                'redis>=5.0.0',
                'django-celery-beat>=2.5.0',
                'django-celery-results>=2.5.0',
            ])
        
        return '\n'.join(requirements)
    
    def _render_readme(self) -> str:
        """Render README.md file."""
        return f'''# {self.project_name.replace('_', ' ').title()}

> Generated with [ADEMA Framework](https://github.com/Excel-ente/django-adema)

## Quick Start

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\\Scripts\\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Project Structure

```
{self.project_name}/
├── config/                 # Configuration
│   ├── settings/
│   │   ├── base.py        # Shared settings
│   │   ├── local.py       # Development
│   │   └── production.py  # Production
│   ├── urls.py
│   └── wsgi.py
├── apps/                   # Application modules
├── templates/              # HTML templates
├── static/                 # Static files
├── media/                  # User uploads
├── manage.py
└── requirements.txt
```

## License

MIT
'''
    
    def _render_base_settings(self) -> str:
        """Render base.py settings file."""
        return f'''"""
Django Base Settings for {self.project_name}
=============================================

Settings shared between all environments.
Uses python-dotenv for configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# =============================================================================
# PATHS
# =============================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =============================================================================
# ENVIRONMENT CONFIGURATION
# =============================================================================

# Load .env file if it exists
env_file = BASE_DIR / '.env'
if env_file.exists():
    load_dotenv(env_file)

# Helper function to get env variables with defaults
def get_env(key, default=None, cast=str):
    value = os.getenv(key, default)
    if value is None:
        return default
    if cast == bool:
        return value.lower() in ('true', '1', 'yes', 'on')
    elif cast == list:
        return [item.strip() for item in value.split(',') if item.strip()]
    elif cast == int:
        return int(value)
    return value

# =============================================================================
# CORE SETTINGS
# =============================================================================

SECRET_KEY = get_env('SECRET_KEY', '{self.secret_key}')
DEBUG = get_env('DEBUG', False, cast=bool)
ALLOWED_HOSTS = get_env('ALLOWED_HOSTS', 'localhost,127.0.0.1', cast=list)

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # Add third-party apps here
    # 'rest_framework',
    # 'corsheaders',
]

if {str(self.config.get('use_rest_api', False)).capitalize()}:
    THIRD_PARTY_APPS.extend([
        'rest_framework',
        'corsheaders',
    ])

if {str(self.config.get('use_celery', False)).capitalize()}:
    THIRD_PARTY_APPS.append('django_celery_results')

LOCAL_APPS = [
    # Add your apps here
]

# Auto-register selected modules
modules = {self.config.get('modules', [])}
for module in modules:
    if isinstance(module, dict):
        module_name = module.get('name')
    else:
        module_name = module
    
    if module_name:
        LOCAL_APPS.append(f'apps.{{module_name}}')

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',  # Uncomment for CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================================================================
# URL CONFIGURATION
# =============================================================================

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

# =============================================================================
# DATABASE
# =============================================================================

# Parse DATABASE_URL or use default SQLite
db_url = get_env('DATABASE_URL', 'sqlite:///db.sqlite3')
if db_url.startswith('sqlite'):
    DATABASES = {{
        'default': {{
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / db_url.replace('sqlite:///', ''),
        }}
    }}
elif db_url.startswith('postgres'):
    # Parse postgres://user:password@host:port/dbname
    import re
    match = re.match(r'postgres://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', db_url)
    if match:
        DATABASES = {{
            'default': {{
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': match.group(5),
                'USER': match.group(1),
                'PASSWORD': match.group(2),
                'HOST': match.group(3),
                'PORT': match.group(4),
            }}
        }}
    else:
        DATABASES = {{'default': {{'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}}}
else:
    DATABASES = {{'default': {{'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}}}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================================================================
# LOGGING
# =============================================================================

LOGGING = {{
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {{
        'verbose': {{
            'format': '{{levelname}} {{asctime}} {{module}} {{message}}',
            'style': '{{',
        }},
    }},
    'handlers': {{
        'console': {{
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }},
    }},
    'root': {{
        'handlers': ['console'],
        'level': 'INFO',
    }},
}}
'''
    
    def _render_local_settings(self) -> str:
        """Render local.py settings file."""
        return f'''"""
Django Local/Development Settings for {self.project_name}
==========================================================

Settings for local development environment.
"""

from .base import *

# =============================================================================
# DEBUG
# =============================================================================

DEBUG = True

# =============================================================================
# ALLOWED HOSTS
# =============================================================================

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# =============================================================================
# DATABASE (Override for local)
# =============================================================================

# Use SQLite for local development if DATABASE_URL not set
db_url = get_env('DATABASE_URL', 'sqlite:///db.sqlite3')
if db_url.startswith('sqlite'):
    DATABASES = {{
        'default': {{
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / db_url.replace('sqlite:///', ''),
        }}
    }}

# =============================================================================
# EMAIL (Console backend for development)
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# =============================================================================
# DEBUG TOOLBAR (Optional)
# =============================================================================

# Uncomment to enable Django Debug Toolbar
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# INTERNAL_IPS = ['127.0.0.1']

# =============================================================================
# CORS (Development)
# =============================================================================

# CORS_ALLOW_ALL_ORIGINS = True  # Only for development!
'''
    
    def _render_production_settings(self) -> str:
        """Render production.py settings file."""
        return f'''"""
Django Production Settings for {self.project_name}
===================================================

Settings for production environment.
"""

from .base import *

# =============================================================================
# DEBUG
# =============================================================================

DEBUG = False

# =============================================================================
# SECURITY
# =============================================================================

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (uncomment when using HTTPS)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# =============================================================================
# CSRF
# =============================================================================

CSRF_TRUSTED_ORIGINS = get_env('CSRF_TRUSTED_ORIGINS', '', cast=list)

# =============================================================================
# EMAIL (Production)
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = get_env('EMAIL_PORT', 587, cast=int)
EMAIL_USE_TLS = get_env('EMAIL_USE_TLS', True, cast=bool)
EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD', '')

# =============================================================================
# LOGGING (Production)
# =============================================================================

LOGGING['handlers']['file'] = {{
    'class': 'logging.FileHandler',
    'filename': BASE_DIR / 'logs' / 'django.log',
    'formatter': 'verbose',
}}
LOGGING['root']['handlers'].append('file')
'''
    
    def preview_settings(self) -> str:
        """
        Generate a preview of the settings file without creating the project.
        
        Returns:
            The rendered base.py settings content.
        """
        return self._render_base_settings()


class AppBuilder:
    """
    Builds an ADEMA app module with vertical slicing structure.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the app builder.
        
        Args:
            config: App configuration dictionary containing:
                - name: App name
                - output_dir: Where to create the app
        """
        self.config = config
        self.app_name = config.get('name', 'my_app')
        self.output_dir = Path(config.get('output_dir', './apps')).resolve()
        self.app_dir = self.output_dir / self.app_name
    
    def _write_file(self, path: Path, content: str) -> None:
        """
        Write content to file with UTF-8 encoding.
        
        This ensures proper handling of special characters on Windows.
        """
        path.write_text(content, encoding='utf-8')
    
    def build(self) -> str:
        """
        Build the complete app module.
        
        Returns:
            Path to the created app directory.
        """
        if self.app_dir.exists():
            raise ValueError(f"Directory already exists: {self.app_dir}")
        
        # Create directory structure
        self._create_directory_structure()
        
        # Generate files
        self._generate_init()
        self._generate_apps()
        self._generate_models()
        self._generate_views()
        self._generate_urls()
        self._generate_admin()
        self._generate_components()
        self._generate_services()
        
        return str(self.app_dir)
    
    def _create_directory_structure(self):
        """Create the app directory structure."""
        directories = [
            self.app_dir,
            self.app_dir / 'views',
            self.app_dir / 'components',
            self.app_dir / 'services',
            self.app_dir / 'admin',
            self.app_dir / 'templates' / self.app_name,
            self.app_dir / 'migrations',
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _generate_init(self):
        """Generate __init__.py files."""
        self._write_file(self.app_dir / '__init__.py', '')
        self._write_file(self.app_dir / 'views' / '__init__.py', '')
        self._write_file(self.app_dir / 'components' / '__init__.py', '')
        self._write_file(self.app_dir / 'services' / '__init__.py', '')
        self._write_file(self.app_dir / 'admin' / '__init__.py', '')
        self._write_file(self.app_dir / 'migrations' / '__init__.py', '')
    
    def _generate_apps(self):
        """Generate apps.py."""
        camel_case = ''.join(word.title() for word in self.app_name.split('_'))
        content = f'''"""
App Configuration for {self.app_name}
"""
from django.apps import AppConfig


class {camel_case}Config(AppConfig):
    """Configuration for the {self.app_name} app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{self.app_name}'
    verbose_name = '{self.app_name.replace("_", " ").title()}'
    
    def ready(self):
        """Run when the app is ready."""
        # Import signals here if needed
        pass
'''
        self._write_file(self.app_dir / 'apps.py', content)
    
    def _generate_models(self):
        """Generate models.py."""
        content = f'''"""
Models for {self.app_name}
===========================

All models inherit from AdemaBaseModel which provides:
- UUID primary key
- created_at, updated_at timestamps
- is_active for soft delete
"""
from django.db import models

try:
    from adema.base.models import AdemaBaseModel
except ImportError:
    # Fallback if adema is not installed
    import uuid
    
    class AdemaBaseModel(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        is_active = models.BooleanField(default=True)
        
        class Meta:
            abstract = True


# =============================================================================
# YOUR MODELS HERE
# =============================================================================

# Example:
# class {self.app_name.title().replace("_", "")}Item(AdemaBaseModel):
#     """Example model."""
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     
#     class Meta:
#         verbose_name = '{self.app_name.replace("_", " ")} item'
#         verbose_name_plural = '{self.app_name.replace("_", " ")} items'
#         ordering = ['-created_at']
#     
#     def __str__(self):
#         return self.name
'''
        self._write_file(self.app_dir / 'models.py', content)
    
    def _generate_views(self):
        """Generate views."""
        content = f'''"""
Views for {self.app_name}
==========================
"""
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# =============================================================================
# YOUR VIEWS HERE
# =============================================================================

def index(request):
    """Index view for {self.app_name}."""
    context = {{
        'title': '{self.app_name.replace("_", " ").title()}',
    }}
    return render(request, '{self.app_name}/index.html', context)
'''
        self._write_file(self.app_dir / 'views' / '__init__.py', content)
    
    def _generate_urls(self):
        """Generate urls.py."""
        content = f'''"""
URL Configuration for {self.app_name}
======================================
"""
from django.urls import path
from .views import index

app_name = '{self.app_name}'

urlpatterns = [
    path('', index, name='index'),
    # Add your URL patterns here
]
'''
        self._write_file(self.app_dir / 'urls.py', content)
    
    def _generate_admin(self):
        """Generate admin configuration."""
        content = f'''"""
Admin Configuration for {self.app_name}
========================================
"""
from django.contrib import admin
# from .models import YourModel


# =============================================================================
# ADMIN REGISTRATION
# =============================================================================

# @admin.register(YourModel)
# class YourModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'is_active', 'created_at']
#     list_filter = ['is_active', 'created_at']
#     search_fields = ['name']
#     ordering = ['-created_at']
'''
        self._write_file(self.app_dir / 'admin' / '__init__.py', content)
    
    def _generate_components(self):
        """Generate components configuration."""
        content = f'''"""
Components (Entidades/Modelos) para {self.app_name}
===================================================

Cada entidad del módulo debe definirse en su propio archivo.
Ejemplo: producto.py, categoria.py, cliente.py, etc.

Los modelos se importan automáticamente desde aquí hacia models.py

Generated by ADEMA Framework.
"""

# Importa aquí tus modelos para exponerlos al módulo
# from .example_model import ExampleModel

# Al agregar nuevos modelos:
# 1. Crea un archivo: components/mi_entidad.py
# 2. Define tu modelo heredando de AdemaBaseModel
# 3. Importa aquí: from .mi_entidad import MiEntidad
# 4. Ejecuta: python manage.py makemigrations && python manage.py migrate


# =============================================================================
# EJEMPLO DE MODELO COMPLETO (Referencia)
# =============================================================================
#
# Copia y adapta este código en un nuevo archivo (ej: components/producto.py)
#
# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from adema.base.models import AdemaBaseModel
#
# class Categoria(AdemaBaseModel):
#     """Categoría de productos."""
#     nombre = models.CharField(_('Nombre'), max_length=100)
#     slug = models.SlugField(unique=True)
#
#     class Meta:
#         verbose_name = _('Categoría')
#         verbose_name_plural = _('Categorías')
#
#     def __str__(self):
#         return self.nombre
#
#
# class Producto(AdemaBaseModel):
#     """
#     Modelo de Producto para el inventario.
#     """
#     
#     # Campos de datos
#     nombre = models.CharField(
#         _('Nombre'), 
#         max_length=255,
#         help_text=_('Nombre del producto')
#     )
#     
#     codigo = models.CharField(
#         _('Código'), 
#         max_length=50, 
#         unique=True,
#         help_text=_('Código único de identificación (SKU)')
#     )
#     
#     descripcion = models.TextField(
#         _('Descripción'), 
#         blank=True,
#         help_text=_('Descripción detallada del producto')
#     )
#     
#     precio = models.DecimalField(
#         _('Precio'), 
#         max_digits=10, 
#         decimal_places=2,
#         default=0.00
#     )
#     
#     stock = models.IntegerField(
#         _('Stock'), 
#         default=0,
#         help_text=_('Cantidad disponible')
#     )
#     
#     # Relaciones
#     categoria = models.ForeignKey(
#         'Categoria', 
#         on_delete=models.PROTECT,
#         related_name='productos',
#         verbose_name=_('Categoría'),
#         null=True, blank=True
#     )
#     
#     # Choices
#     ESTADO_DISPONIBLE = 'disponible'
#     ESTADO_AGOTADO = 'agotado'
#     ESTADO_CHOICES = [
#         (ESTADO_DISPONIBLE, _('Disponible')),
#         (ESTADO_AGOTADO, _('Agotado')),
#     ]
#     
#     estado = models.CharField(
#         _('Estado'),
#         max_length=20,
#         choices=ESTADO_CHOICES,
#         default=ESTADO_DISPONIBLE
#     )
#
#     class Meta:
#         verbose_name = _('Producto')
#         verbose_name_plural = _('Productos')
#         ordering = ['nombre']
#         # Permisos personalizados
#         permissions = [
#             ("can_change_stock", "Can change stock"),
#             ("can_view_cost", "Can view cost price"),
#             ("can_export_data", "Can export product data"),
#         ]
#
#     def __str__(self):
#         return f"{{self.codigo}} - {{self.nombre}}"
#
#     def clean(self):
#         """Validaciones personalizadas."""
#         from django.core.exceptions import ValidationError
#         if self.precio < 0:
#             raise ValidationError({{'precio': _('El precio no puede ser negativo.')}})
#
#     @property
#     def is_available(self):
#         return self.stock > 0 and self.estado == self.ESTADO_DISPONIBLE
#
#
# =============================================================================
# EJEMPLO DE ADMIN (Para admin/__init__.py o admin/producto.py)
# =============================================================================
#
# @admin.register(Producto)
# class ProductoAdmin(AdemaModelAdmin):
#     list_display = ['codigo', 'nombre', 'precio', 'stock', 'estado', 'is_available']
#     list_filter = ['estado', 'categoria', 'created_at']
#     search_fields = ['codigo', 'nombre', 'descripcion']
#     list_editable = ['precio', 'stock']
#     readonly_fields = ['created_at', 'updated_at']
#     
#     fieldsets = (
#         (_('Información Principal'), {{
#             'fields': ('codigo', 'nombre', 'categoria', 'estado')
#         }}),
#         (_('Detalles'), {{
#             'fields': ('descripcion', 'precio', 'stock')
#         }}),
#         (_('Metadatos'), {{
#             'fields': ('created_at', 'updated_at', 'id'),
#             'classes': ('collapse',)
#         }}),
#     )
'''
        self._write_file(self.app_dir / 'components' / '__init__.py', content)
    
    def _generate_services(self):
        """Generate services."""
        content = f'''"""
Business Logic Services for {self.app_name}
============================================

Services contain business logic separated from views.
"""
try:
    from adema.base.services import AdemaBaseService
except ImportError:
    import logging
    
    class AdemaBaseService:
        """Fallback base service if adema is not installed."""
        
        def __init__(self):
            self.log = logging.getLogger(self.__class__.__name__)


# =============================================================================
# YOUR SERVICES HERE
# =============================================================================

# Example:
# class {self.app_name.title().replace("_", "")}Service(AdemaBaseService):
#     """Service for {self.app_name} business logic."""
#     
#     def process_item(self, item_id):
#         self.log.info(f"Processing item {{item_id}}")
#         # Your business logic here
#         pass
'''
        self._write_file(self.app_dir / 'services' / '__init__.py', content)
        
        # Create index template
        template_content = '''{% extends "base.html" %}

{% block title %}''' + self.app_name.replace("_", " ").title() + '''{% endblock %}

{% block content %}
<div class="container">
    <h1>''' + self.app_name.replace("_", " ").title() + '''</h1>
    <p>Welcome to the ''' + self.app_name + ''' module.</p>
</div>
{% endblock %}
'''
        self._write_file(self.app_dir / 'templates' / self.app_name / 'index.html', template_content)

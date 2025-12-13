"""
ADEMA Framework - Django Project Generator
==========================================

A meta-framework and CLI tool for generating Django projects 
with a "Vertical Slicing" architecture optimized for ERP/CRM applications.

Installation:
    pip install django-adema

Usage:
    django-adema startproject <name>    # Quick headless generation
    django-adema startapp <name>        # Create a new app module
    django-adema launch                 # Interactive Web Wizard UI
"""

from setuptools import setup, find_packages

# Read the README for the long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = __doc__

setup(
    name='django-adema',
    version='0.1.0',
    author='ADEMA Team',
    author_email='info@adema.dev',
    description='Django meta-framework for generating ERP/CRM projects with Vertical Slicing architecture',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Excel-ente/django-adema',
    license='MIT',
    
    packages=find_packages(),
    include_package_data=True,  # CRUCIAL: Para que MANIFEST.in funcione
    
    python_requires='>=3.9',
    
    install_requires=[
        # Django Core
        'Django>=4.2',
        'python-dotenv>=1.0.0',
        'psycopg2-binary>=2.9.9',
        
        # CLI
        'typer[all]>=0.9.0',
        'rich>=13.0.0',
        
        # Web Wizard UI
        'fastapi>=0.104.0',
        'uvicorn[standard]>=0.24.0',
        
        # Template Engine
        'Jinja2>=3.1.2',
    ],
    
    extras_require={
        'dev': [
            'black',
            'isort',
            'flake8',
            'pytest',
            'pytest-django',
            'twine',
            'build',
        ],
        'ai': [
            'langchain>=0.1.0',
            'langchain-community>=0.0.10',
            'langchain-openai>=0.1.0',
        ],
    },
    
    entry_points={
        'console_scripts': [
            'django-adema=adema.cli:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    
    keywords='django, framework, erp, crm, scaffolding, generator, vertical-slicing',
    
    project_urls={
        'Documentation': 'https://github.com/Excel-ente/django-adema#readme',
        'Source': 'https://github.com/Excel-ente/django-adema',
        'Tracker': 'https://github.com/Excel-ente/django-adema/issues',
    },
)

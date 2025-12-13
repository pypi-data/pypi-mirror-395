"""
ADEMA Web Wizard Server
=======================

FastAPI server for the interactive Web Wizard UI.
Provides endpoints for configuring and generating ADEMA projects.
"""

import os
import json
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field


# =============================================================================
# Pydantic Models for API
# =============================================================================

class DatabaseConfig(BaseModel):
    """Database configuration model."""
    engine: str = Field(default="sqlite", description="Database engine: sqlite, postgres")
    name: str = Field(default="db.sqlite3", description="Database name")
    host: Optional[str] = Field(default="localhost", description="Database host")
    port: Optional[int] = Field(default=5432, description="Database port")
    user: Optional[str] = Field(default="", description="Database user")
    password: Optional[str] = Field(default="", description="Database password")


class ModuleConfig(BaseModel):
    """Module configuration for an app."""
    name: str = Field(..., description="Module name")
    label: str = Field(..., description="Human-readable label")
    enabled: bool = Field(default=True, description="Whether to include this module")


class FieldConfig(BaseModel):
    """Field configuration for model generation."""
    name: str = Field(..., description="Field name")
    field_type: str = Field(..., description="Django field type")
    required: bool = Field(default=True, description="Whether field is required")
    max_length: Optional[int] = Field(default=None, description="Max length for CharField")
    choices: Optional[List[str]] = Field(default=None, description="Choices for ChoiceField")


class ModelConfig(BaseModel):
    """Model configuration for generation."""
    name: str = Field(..., description="Model name")
    fields: List[FieldConfig] = Field(default=[], description="Model fields")
    inherit_base: bool = Field(default=True, description="Inherit from AdemaBaseModel")


class ProjectConfig(BaseModel):
    """Complete project configuration."""
    name: str = Field(..., description="Project name")
    description: str = Field(default="", description="Project description")
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    modules: List[ModuleConfig] = Field(default=[], description="Modules to include")
    models: List[ModelConfig] = Field(default=[], description="Custom models to generate")
    output_dir: str = Field(default=".", description="Output directory")
    
    # Additional options
    use_celery: bool = Field(default=False, description="Include Celery configuration")
    use_docker: bool = Field(default=False, description="Generate Docker files")
    use_rest_api: bool = Field(default=False, description="Include DRF setup")
    include_ai: bool = Field(default=False, description="Include AI Agents support")


class GenerationResult(BaseModel):
    """Result of project generation."""
    status: str
    message: str
    project_path: Optional[str] = None
    errors: List[str] = Field(default=[])


# =============================================================================
# FastAPI Application
# =============================================================================

app = FastAPI(
    title="ADEMA Web Wizard",
    description="Interactive project configuration and generation wizard",
    version="0.1.0",
)

# Get paths to static and template directories
UI_DIR = Path(__file__).parent
STATIC_DIR = UI_DIR / "static"
TEMPLATES_DIR = UI_DIR / "templates"

# Mount static files (CSS, JS)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR)) if TEMPLATES_DIR.exists() else None


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main wizard page."""
    if templates is None:
        return HTMLResponse(content=get_fallback_html(), status_code=200)
    
    return templates.TemplateResponse("wizard.html", {
        "request": request,
        "title": "ADEMA Web Wizard",
    })


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


@app.get("/api/modules")
async def get_available_modules():
    """
    Get list of available modules.
    
    Descubre módulos dinámicamente desde:
    1. Módulos built-in (templates)
    2. Módulos instalados via entry_points (adema-ventas, adema-compras, etc.)
    """
    from adema.modules import registry, discover_modules
    from adema.modules.config import get_config
    
    # Descubrir módulos automáticamente
    discover_modules()
    
    # Obtener configuración
    config = get_config()
    
    # Filtrar módulos habilitados
    modules_list = []
    for module in registry.get_modules_list():
        if config.is_module_enabled(module['name']):
            modules_list.append(module)
    
    return {"modules": modules_list}


@app.get("/api/modules/{module_name}")
async def get_module_info(module_name: str):
    """
    Get detailed information about a specific module.
    
    Args:
        module_name: Name of the module to get info for
    """
    from adema.modules import registry, discover_modules
    
    discover_modules()
    
    module = registry.get_module(module_name)
    if not module:
        raise HTTPException(status_code=404, detail=f"Module '{module_name}' not found")
    
    return module.to_dict()


@app.get("/api/modules/category/{category}")
async def get_modules_by_category(category: str):
    """
    Get modules filtered by category.
    
    Categories: erp, crm, finance, hr, utils, general
    """
    from adema.modules import registry, discover_modules
    from adema.modules.config import get_config, DEFAULT_CATEGORIES
    
    discover_modules()
    config = get_config()
    
    modules = registry.get_modules_by_category(category)
    modules_list = [
        m.to_dict() for m in modules 
        if config.is_module_enabled(m.name)
    ]
    
    category_info = DEFAULT_CATEGORIES.get(category, {})
    
    return {
        "category": category,
        "category_info": {
            "label": getattr(category_info, 'label', category.title()),
            "description": getattr(category_info, 'description', ''),
            "icon": getattr(category_info, 'icon', '📦'),
        } if category_info else {},
        "modules": modules_list,
    }


@app.get("/api/field-types")
async def get_field_types():
    """Get available Django field types for model builder."""
    return {
        "field_types": [
            {"type": "CharField", "label": "Texto", "requires_max_length": True},
            {"type": "TextField", "label": "Texto Largo", "requires_max_length": False},
            {"type": "IntegerField", "label": "Número Entero", "requires_max_length": False},
            {"type": "DecimalField", "label": "Número Decimal", "requires_max_length": False},
            {"type": "BooleanField", "label": "Booleano (Sí/No)", "requires_max_length": False},
            {"type": "DateField", "label": "Fecha", "requires_max_length": False},
            {"type": "DateTimeField", "label": "Fecha y Hora", "requires_max_length": False},
            {"type": "EmailField", "label": "Email", "requires_max_length": False},
            {"type": "URLField", "label": "URL", "requires_max_length": False},
            {"type": "FileField", "label": "Archivo", "requires_max_length": False},
            {"type": "ImageField", "label": "Imagen", "requires_max_length": False},
            {"type": "ForeignKey", "label": "Relación (FK)", "requires_max_length": False},
        ]
    }


@app.post("/api/generate", response_model=GenerationResult)
async def generate_project(config: ProjectConfig):
    """
    Generate a new ADEMA project with the provided configuration.
    
    This is the main endpoint called when the user clicks "Generate"
    in the Web Wizard.
    """
    try:
        from adema.generator.project_builder import ProjectBuilder
        
        # Convert Pydantic model to dict
        config_dict = config.model_dump()
        
        # Create the project using the builder
        builder = ProjectBuilder(config_dict)
        result_path = builder.build()
        
        return GenerationResult(
            status="success",
            message=f"Project '{config.name}' created successfully!",
            project_path=result_path,
        )
        
    except ImportError as e:
        return GenerationResult(
            status="error",
            message="Generator module not available",
            errors=[str(e)],
        )
    except Exception as e:
        return GenerationResult(
            status="error",
            message="Failed to generate project",
            errors=[str(e)],
        )


@app.post("/api/preview")
async def preview_settings(config: ProjectConfig):
    """
    Preview the generated settings.py content without creating files.
    Useful for reviewing configuration before generation.
    """
    try:
        from adema.generator.project_builder import ProjectBuilder
        
        builder = ProjectBuilder(config.model_dump())
        preview = builder.preview_settings()
        
        return {"status": "ok", "content": preview}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}


# =============================================================================
# Fallback HTML (if templates not available)
# =============================================================================

def get_fallback_html() -> str:
    """Return a basic HTML page if templates are not found."""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ADEMA Web Wizard</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); min-height: 100vh; }
            .wizard-container { max-width: 800px; margin: 50px auto; }
            .card { border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
            .btn-adema { background: #27ae60; border: none; }
            .btn-adema:hover { background: #219a52; }
            .module-item { padding: 10px; border: 1px solid #dee2e6; border-radius: 8px; margin-bottom: 8px; }
            .module-item:hover { background: #f8f9fa; }
            .module-icon { font-size: 1.5em; margin-right: 10px; }
            .module-category { font-size: 0.75em; color: #6c757d; }
            .loading { text-align: center; padding: 20px; }
        </style>
    </head>
    <body>
        <div class="wizard-container">
            <div class="card">
                <div class="card-header bg-dark text-white text-center py-4">
                    <h1>🏭 ADEMA Web Wizard</h1>
                    <p class="mb-0">Generador de Proyectos Django</p>
                </div>
                <div class="card-body p-4">
                    <form id="projectForm">
                        <div class="mb-3">
                            <label class="form-label">Nombre del Proyecto</label>
                            <input type="text" class="form-control" id="projectName" placeholder="mi_erp" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Base de Datos</label>
                            <select class="form-select" id="database">
                                <option value="sqlite">SQLite (Desarrollo)</option>
                                <option value="postgres">PostgreSQL (Producción)</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Módulos Disponibles</label>
                            <div id="modulesContainer" class="loading">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Cargando módulos...</span>
                                </div>
                                <p class="mt-2">Descubriendo módulos...</p>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Directorio de Salida</label>
                            <input type="text" class="form-control" id="outputDir" value=".">
                        </div>
                        
                        <button type="submit" class="btn btn-adema btn-lg w-100 text-white">
                            🚀 Generar Proyecto
                        </button>
                    </form>
                    
                    <div id="result" class="mt-4" style="display: none;"></div>
                </div>
            </div>
        </div>
        
        <script>
            // Cargar módulos dinámicamente desde la API
            async function loadModules() {
                const container = document.getElementById('modulesContainer');
                try {
                    const response = await fetch('/api/modules');
                    const data = await response.json();
                    
                    if (data.modules && data.modules.length > 0) {
                        container.innerHTML = data.modules.map(module => `
                            <div class="module-item">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" 
                                           value="${module.name}" 
                                           id="mod_${module.name}"
                                           data-label="${module.label}">
                                    <label class="form-check-label" for="mod_${module.name}">
                                        <span class="module-icon">${module.icon || '📦'}</span>
                                        <strong>${module.label}</strong>
                                        <span class="module-category">(${module.category || 'general'})</span>
                                        <br>
                                        <small class="text-muted">${module.description || ''}</small>
                                    </label>
                                </div>
                            </div>
                        `).join('');
                    } else {
                        container.innerHTML = '<p class="text-muted">No hay módulos disponibles</p>';
                    }
                } catch (err) {
                    container.innerHTML = `<div class="alert alert-warning">
                        Error cargando módulos: ${err.message}
                    </div>`;
                }
            }
            
            // Cargar módulos al iniciar
            document.addEventListener('DOMContentLoaded', loadModules);
            
            document.getElementById('projectForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const modules = [];
                document.querySelectorAll('#modulesContainer input[type="checkbox"]:checked').forEach(cb => {
                    modules.push({
                        name: cb.value, 
                        label: cb.dataset.label || cb.value, 
                        enabled: true
                    });
                });
                
                const config = {
                    name: document.getElementById('projectName').value,
                    database: {
                        engine: document.getElementById('database').value,
                        name: document.getElementById('database').value === 'sqlite' ? 'db.sqlite3' : document.getElementById('projectName').value
                    },
                    modules: modules,
                    output_dir: document.getElementById('outputDir').value
                };
                
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '<div class="alert alert-info">Generando proyecto...</div>';
                
                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(config)
                    });
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        resultDiv.innerHTML = `<div class="alert alert-success">
                            ✅ ${data.message}<br>
                            <small>Path: ${data.project_path}</small>
                        </div>`;
                    } else {
                        resultDiv.innerHTML = `<div class="alert alert-danger">
                            ❌ ${data.message}<br>
                            <small>${data.errors.join(', ')}</small>
                        </div>`;
                    }
                } catch (err) {
                    resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
                }
            });
        </script>
    </body>
    </html>
    """


# =============================================================================
# Server Startup
# =============================================================================

def start_server(host: str = "127.0.0.1", port: int = 8765):
    """Start the FastAPI server using Uvicorn."""
    import uvicorn
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    start_server()

/**
 * ADEMA Web Wizard JavaScript
 * Handles multi-step form navigation and project generation
 */

class AdemWizard {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.config = {
            name: '',
            description: '',
            database: {
                engine: 'sqlite',
                name: 'db.sqlite3',
                host: 'localhost',
                port: 5432,
                user: '',
                password: ''
            },
            modules: [],
            models: [],
            output_dir: '.',
            use_celery: false,
            use_docker: false,
            use_rest_api: false,
            include_ai: false
        };
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadAvailableModules();
        this.updateStepDisplay();
    }
    
    bindEvents() {
        // Step navigation
        document.querySelectorAll('.step').forEach(step => {
            step.addEventListener('click', (e) => {
                const stepNum = parseInt(e.currentTarget.dataset.step);
                if (stepNum <= this.getMaxAllowedStep()) {
                    this.goToStep(stepNum);
                }
            });
        });
        
        // Next/Prev buttons
        document.querySelectorAll('[data-action="next"]').forEach(btn => {
            btn.addEventListener('click', () => this.nextStep());
        });
        
        document.querySelectorAll('[data-action="prev"]').forEach(btn => {
            btn.addEventListener('click', () => this.prevStep());
        });
        
        // Generate button
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generateProject());
        }
        
        // Form inputs
        document.getElementById('projectName')?.addEventListener('input', (e) => {
            this.config.name = e.target.value;
        });
        
        document.getElementById('projectDesc')?.addEventListener('input', (e) => {
            this.config.description = e.target.value;
        });
        
        document.getElementById('dbEngine')?.addEventListener('change', (e) => {
            this.config.database.engine = e.target.value;
            this.toggleDatabaseFields();
        });
        
        document.getElementById('outputDir')?.addEventListener('input', (e) => {
            this.config.output_dir = e.target.value;
        });
        
        // Checkbox cards
        document.querySelectorAll('.checkbox-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const checkbox = card.querySelector('input[type="checkbox"]');
                if (e.target !== checkbox) {
                    checkbox.checked = !checkbox.checked;
                }
                card.classList.toggle('selected', checkbox.checked);
                this.updateModuleSelection();
            });
        });
        
        // Add model button
        document.getElementById('addModelBtn')?.addEventListener('click', () => {
            this.showModelDialog();
        });
    }
    
    getMaxAllowedStep() {
        // Can only go to steps that have been completed or are current
        return this.currentStep;
    }
    
    goToStep(step) {
        if (step < 1 || step > this.totalSteps) return;
        
        // Validate current step before proceeding
        if (step > this.currentStep && !this.validateStep(this.currentStep)) {
            return;
        }
        
        this.currentStep = step;
        this.updateStepDisplay();
    }
    
    nextStep() {
        if (this.validateStep(this.currentStep)) {
            this.goToStep(this.currentStep + 1);
        }
    }
    
    prevStep() {
        this.goToStep(this.currentStep - 1);
    }
    
    validateStep(step) {
        switch (step) {
            case 1:
                if (!this.config.name || this.config.name.trim() === '') {
                    this.showError('Por favor ingresa un nombre para el proyecto');
                    return false;
                }
                if (!/^[a-z][a-z0-9_]*$/.test(this.config.name)) {
                    this.showError('El nombre debe empezar con letra minúscula y contener solo letras, números y guiones bajos');
                    return false;
                }
                break;
            case 2:
                // Database config - optional validation
                break;
            case 3:
                // Modules - optional
                break;
        }
        return true;
    }
    
    updateStepDisplay() {
        // Update step indicators
        document.querySelectorAll('.step').forEach(step => {
            const stepNum = parseInt(step.dataset.step);
            step.classList.remove('active', 'completed');
            
            if (stepNum === this.currentStep) {
                step.classList.add('active');
            } else if (stepNum < this.currentStep) {
                step.classList.add('completed');
            }
        });
        
        // Update form sections
        document.querySelectorAll('.form-section').forEach(section => {
            section.classList.remove('active');
        });
        
        const currentSection = document.querySelector(`.form-section[data-step="${this.currentStep}"]`);
        if (currentSection) {
            currentSection.classList.add('active');
        }
        
        // Update navigation buttons
        this.updateNavButtons();
    }
    
    updateNavButtons() {
        const prevBtn = document.querySelector('[data-action="prev"]');
        const nextBtn = document.querySelector('[data-action="next"]');
        const generateBtn = document.getElementById('generateBtn');
        
        if (prevBtn) {
            prevBtn.style.display = this.currentStep > 1 ? 'block' : 'none';
        }
        
        if (nextBtn) {
            nextBtn.style.display = this.currentStep < this.totalSteps ? 'block' : 'none';
        }
        
        if (generateBtn) {
            generateBtn.style.display = this.currentStep === this.totalSteps ? 'block' : 'none';
        }
    }
    
    toggleDatabaseFields() {
        const postgresFields = document.getElementById('postgresFields');
        if (postgresFields) {
            postgresFields.style.display = this.config.database.engine === 'postgres' ? 'block' : 'none';
        }
    }
    
    async loadAvailableModules() {
        try {
            const response = await fetch('/api/modules');
            const data = await response.json();
            this.renderModules(data.modules);
        } catch (error) {
            console.error('Error loading modules:', error);
        }
    }
    
    renderModules(modules) {
        const container = document.getElementById('modulesContainer');
        if (!container) return;
        
        container.innerHTML = modules.map(mod => `
            <div class="checkbox-card" data-module="${mod.name}">
                <input type="checkbox" name="modules" value="${mod.name}">
                <div class="checkbox-card-title">${mod.label}</div>
                <div class="checkbox-card-desc">${mod.description}</div>
            </div>
        `).join('');
        
        // Re-bind events for new cards
        container.querySelectorAll('.checkbox-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const checkbox = card.querySelector('input[type="checkbox"]');
                if (e.target !== checkbox) {
                    checkbox.checked = !checkbox.checked;
                }
                card.classList.toggle('selected', checkbox.checked);
                this.updateModuleSelection();
            });
        });
    }
    
    updateModuleSelection() {
        this.config.modules = [];
        document.querySelectorAll('.checkbox-card.selected').forEach(card => {
            const moduleName = card.dataset.module;
            if (moduleName) {
                this.config.modules.push({
                    name: moduleName,
                    label: moduleName,
                    enabled: true
                });
            }
        });
    }
    
    showModelDialog() {
        // Simple prompt for now - can be enhanced with a modal
        const modelName = prompt('Nombre del modelo (ej: Producto, Cliente):');
        if (modelName) {
            this.config.models.push({
                name: modelName,
                fields: [],
                inherit_base: true
            });
            this.renderModels();
        }
    }
    
    renderModels() {
        const container = document.getElementById('modelsList');
        if (!container) return;
        
        container.innerHTML = this.config.models.map((model, idx) => `
            <div class="model-item">
                <div>
                    <strong>${model.name}</strong>
                    <span class="badge">(AdemaBaseModel)</span>
                </div>
                <button class="btn btn-danger btn-sm" onclick="wizard.removeModel(${idx})">
                    Eliminar
                </button>
            </div>
        `).join('');
    }
    
    removeModel(index) {
        this.config.models.splice(index, 1);
        this.renderModels();
    }
    
    async generateProject() {
        const resultPanel = document.getElementById('resultPanel');
        if (resultPanel) {
            resultPanel.className = 'result-panel loading';
            resultPanel.innerHTML = '⏳ Generando proyecto...';
            resultPanel.style.display = 'block';
        }
        
        try {
            // Collect all form data
            this.collectFormData();
            
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.config)
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                resultPanel.className = 'result-panel success';
                resultPanel.innerHTML = `
                    <h4>✅ ¡Proyecto creado exitosamente!</h4>
                    <p>${result.message}</p>
                    <p><strong>Ubicación:</strong> ${result.project_path}</p>
                    <hr>
                    <p>Próximos pasos:</p>
                    <div class="code-preview">
cd ${this.config.name}
python -m venv venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
                    </div>
                `;
            } else {
                resultPanel.className = 'result-panel error';
                resultPanel.innerHTML = `
                    <h4>❌ Error al generar el proyecto</h4>
                    <p>${result.message}</p>
                    ${result.errors ? `<ul>${result.errors.map(e => `<li>${e}</li>`).join('')}</ul>` : ''}
                `;
            }
        } catch (error) {
            resultPanel.className = 'result-panel error';
            resultPanel.innerHTML = `
                <h4>❌ Error de conexión</h4>
                <p>${error.message}</p>
            `;
        }
    }
    
    collectFormData() {
        // Collect project info
        this.config.name = document.getElementById('projectName')?.value || this.config.name;
        this.config.description = document.getElementById('projectDesc')?.value || '';
        this.config.output_dir = document.getElementById('outputDir')?.value || '.';
        
        // Collect database config
        this.config.database.engine = document.getElementById('dbEngine')?.value || 'sqlite';
        
        if (this.config.database.engine === 'postgres') {
            this.config.database.name = document.getElementById('dbName')?.value || this.config.name;
            this.config.database.host = document.getElementById('dbHost')?.value || 'localhost';
            this.config.database.port = parseInt(document.getElementById('dbPort')?.value) || 5432;
            this.config.database.user = document.getElementById('dbUser')?.value || '';
            this.config.database.password = document.getElementById('dbPassword')?.value || '';
        } else {
            this.config.database.name = 'db.sqlite3';
        }
        
        // Collect options
        this.config.use_celery = document.getElementById('useCelery')?.checked || false;
        this.config.use_docker = document.getElementById('useDocker')?.checked || false;
        this.config.use_rest_api = document.getElementById('useRestApi')?.checked || false;
        this.config.include_ai = document.getElementById('includeAi')?.checked || false;
    }
    
    showError(message) {
        alert(message); // Simple for now - can be enhanced with toast notifications
    }
}

// Initialize wizard on page load
let wizard;
document.addEventListener('DOMContentLoaded', () => {
    wizard = new AdemWizard();
});

"""
ADEMA Model Builder
===================

Generates Django model code from configuration.
Used by the Web Wizard to create models dynamically.
"""

from typing import Dict, Any, List, Optional


class ModelBuilder:
    """
    Builds Django model code from a configuration dictionary.
    
    This class generates Python code for Django models based on
    field definitions provided by the Web Wizard UI.
    """
    
    FIELD_TYPE_MAP = {
        'CharField': 'models.CharField',
        'TextField': 'models.TextField',
        'IntegerField': 'models.IntegerField',
        'DecimalField': 'models.DecimalField',
        'BooleanField': 'models.BooleanField',
        'DateField': 'models.DateField',
        'DateTimeField': 'models.DateTimeField',
        'EmailField': 'models.EmailField',
        'URLField': 'models.URLField',
        'FileField': 'models.FileField',
        'ImageField': 'models.ImageField',
        'ForeignKey': 'models.ForeignKey',
        'SlugField': 'models.SlugField',
        'UUIDField': 'models.UUIDField',
        'JSONField': 'models.JSONField',
        'PositiveIntegerField': 'models.PositiveIntegerField',
        'FloatField': 'models.FloatField',
    }
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the model builder.
        
        Args:
            config: Model configuration containing:
                - name: Model name (PascalCase)
                - fields: List of field configurations
                - inherit_base: Whether to inherit from AdemaBaseModel
                - meta: Optional Meta class configuration
        """
        self.config = config
        self.model_name = config.get('name', 'MyModel')
        self.fields = config.get('fields', [])
        self.inherit_base = config.get('inherit_base', True)
        self.meta = config.get('meta', {})
    
    def build(self) -> str:
        """
        Generate the complete model code.
        
        Returns:
            Python code string for the model.
        """
        lines = []
        
        # Class definition
        base_class = 'AdemaBaseModel' if self.inherit_base else 'models.Model'
        lines.append(f'class {self.model_name}({base_class}):')
        
        # Docstring
        description = self.config.get('description', f'{self.model_name} model.')
        lines.append(f'    """{description}"""')
        lines.append('')
        
        # Fields
        if self.fields:
            for field in self.fields:
                field_code = self._generate_field(field)
                lines.append(f'    {field_code}')
            lines.append('')
        
        # Meta class
        meta_code = self._generate_meta()
        if meta_code:
            lines.extend(meta_code)
            lines.append('')
        
        # __str__ method
        str_field = self._get_str_field()
        if str_field:
            lines.append('    def __str__(self):')
            lines.append(f'        return self.{str_field}')
        
        return '\n'.join(lines)
    
    def _generate_field(self, field: Dict[str, Any]) -> str:
        """
        Generate code for a single field.
        
        Args:
            field: Field configuration dictionary.
            
        Returns:
            Python code string for the field.
        """
        name = field.get('name', 'field')
        field_type = field.get('field_type', 'CharField')
        required = field.get('required', True)
        
        # Get Django field class
        django_field = self.FIELD_TYPE_MAP.get(field_type, 'models.CharField')
        
        # Build arguments
        args = []
        
        # Handle specific field types
        if field_type == 'CharField':
            max_length = field.get('max_length', 200)
            args.append(f'max_length={max_length}')
        
        elif field_type == 'DecimalField':
            max_digits = field.get('max_digits', 10)
            decimal_places = field.get('decimal_places', 2)
            args.append(f'max_digits={max_digits}')
            args.append(f'decimal_places={decimal_places}')
        
        elif field_type == 'ForeignKey':
            related_model = field.get('related_model', 'self')
            on_delete = field.get('on_delete', 'CASCADE')
            args.append(f"'{related_model}'")
            args.append(f'on_delete=models.{on_delete}')
            
            related_name = field.get('related_name')
            if related_name:
                args.append(f"related_name='{related_name}'")
        
        elif field_type == 'FileField' or field_type == 'ImageField':
            upload_to = field.get('upload_to', f'{self.model_name.lower()}/')
            args.append(f"upload_to='{upload_to}'")
        
        # Handle blank/null for optional fields
        if not required:
            if field_type in ['CharField', 'TextField', 'EmailField', 'URLField', 'SlugField']:
                args.append('blank=True')
            else:
                args.append('null=True')
                args.append('blank=True')
        
        # Handle choices
        choices = field.get('choices')
        if choices:
            choices_name = f'{name.upper()}_CHOICES'
            args.append(f'choices={choices_name}')
        
        # Handle verbose_name
        verbose_name = field.get('verbose_name')
        if verbose_name:
            args.append(f"verbose_name='{verbose_name}'")
        
        # Handle help_text
        help_text = field.get('help_text')
        if help_text:
            args.append(f"help_text='{help_text}'")
        
        # Handle default value
        default = field.get('default')
        if default is not None:
            if isinstance(default, str):
                args.append(f"default='{default}'")
            elif isinstance(default, bool):
                args.append(f"default={default}")
            else:
                args.append(f"default={default}")
        
        # Build final field code
        args_str = ', '.join(args)
        return f'{name} = {django_field}({args_str})'
    
    def _generate_meta(self) -> List[str]:
        """
        Generate the Meta class.
        
        Returns:
            List of code lines for the Meta class.
        """
        lines = ['    class Meta:']
        has_content = False
        
        # verbose_name
        verbose_name = self.meta.get('verbose_name')
        if verbose_name:
            lines.append(f"        verbose_name = '{verbose_name}'")
            has_content = True
        
        # verbose_name_plural
        verbose_name_plural = self.meta.get('verbose_name_plural')
        if verbose_name_plural:
            lines.append(f"        verbose_name_plural = '{verbose_name_plural}'")
            has_content = True
        
        # ordering
        ordering = self.meta.get('ordering')
        if ordering:
            lines.append(f"        ordering = {ordering}")
            has_content = True
        elif self.inherit_base:
            lines.append("        ordering = ['-created_at']")
            has_content = True
        
        # db_table
        db_table = self.meta.get('db_table')
        if db_table:
            lines.append(f"        db_table = '{db_table}'")
            has_content = True
        
        # unique_together
        unique_together = self.meta.get('unique_together')
        if unique_together:
            lines.append(f"        unique_together = {unique_together}")
            has_content = True
        
        if not has_content:
            return []
        
        return lines
    
    def _get_str_field(self) -> Optional[str]:
        """
        Get the field to use in __str__ method.
        
        Returns:
            Name of the field to use, or None.
        """
        # First, check if explicitly specified
        str_field = self.config.get('str_field')
        if str_field:
            return str_field
        
        # Look for common name fields
        name_fields = ['name', 'title', 'nombre', 'titulo', 'label', 'code', 'codigo']
        
        for field in self.fields:
            field_name = field.get('name', '').lower()
            if field_name in name_fields:
                return field.get('name')
        
        # Return first CharField if exists
        for field in self.fields:
            if field.get('field_type') == 'CharField':
                return field.get('name')
        
        return None
    
    def generate_choices(self) -> str:
        """
        Generate code for field choices.
        
        Returns:
            Python code for choices tuples.
        """
        lines = []
        
        for field in self.fields:
            choices = field.get('choices')
            if choices:
                name = field.get('name', 'field')
                choices_name = f'{name.upper()}_CHOICES'
                
                choices_code = f'{choices_name} = [\n'
                for choice in choices:
                    if isinstance(choice, str):
                        choices_code += f"    ('{choice}', '{choice.title()}'),\n"
                    elif isinstance(choice, (list, tuple)) and len(choice) >= 2:
                        choices_code += f"    ('{choice[0]}', '{choice[1]}'),\n"
                choices_code += ']'
                
                lines.append(choices_code)
        
        return '\n'.join(lines)


def generate_models_file(models: List[Dict[str, Any]]) -> str:
    """
    Generate a complete models.py file from multiple model configurations.
    
    Args:
        models: List of model configuration dictionaries.
        
    Returns:
        Complete Python code for models.py.
    """
    lines = [
        '"""',
        'Models',
        '======',
        '',
        'Auto-generated by ADEMA Framework.',
        '"""',
        'from django.db import models',
        '',
        'try:',
        '    from adema.base.models import AdemaBaseModel',
        'except ImportError:',
        '    import uuid',
        '    ',
        '    class AdemaBaseModel(models.Model):',
        '        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)',
        '        created_at = models.DateTimeField(auto_now_add=True)',
        '        updated_at = models.DateTimeField(auto_now=True)',
        '        is_active = models.BooleanField(default=True)',
        '        ',
        '        class Meta:',
        '            abstract = True',
        '',
        '',
    ]
    
    for model_config in models:
        builder = ModelBuilder(model_config)
        
        # Add choices if any
        choices_code = builder.generate_choices()
        if choices_code:
            lines.append(choices_code)
            lines.append('')
        
        # Add model code
        lines.append(builder.build())
        lines.append('')
        lines.append('')
    
    return '\n'.join(lines)

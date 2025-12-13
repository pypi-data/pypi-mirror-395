"""
ADEMA Admin Mixins
==================

Reusable mixins for Django Admin configuration.
Provides consistent admin experiences across ADEMA apps.

Usage:
    from django.contrib import admin
    from adema.base.admin import AdemaModelAdmin
    from .models import Product
    
    @admin.register(Product)
    class ProductAdmin(AdemaModelAdmin):
        list_display = ['name', 'price'] + AdemaModelAdmin.audit_list_display
"""

from django.contrib import admin
from django.utils.html import format_html


class SoftDeleteAdminMixin:
    """
    Mixin for handling soft-deleted records in admin.
    
    Adds:
        - Filter by active/inactive status
        - Actions for soft delete and restore
        - Visual indication of inactive records
    """
    
    # Show soft-deleted records in admin
    def get_queryset(self, request):
        """Include soft-deleted records in admin."""
        qs = self.model.all_objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
    
    # Admin actions
    actions = ['soft_delete_selected', 'restore_selected', 'hard_delete_selected']
    
    def soft_delete_selected(self, request, queryset):
        """Soft delete selected records."""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} record(s) deactivated.')
    soft_delete_selected.short_description = "Deactivate selected records"
    
    def restore_selected(self, request, queryset):
        """Restore soft-deleted records."""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} record(s) restored.')
    restore_selected.short_description = "Restore selected records"
    
    def hard_delete_selected(self, request, queryset):
        """Permanently delete selected records."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} record(s) permanently deleted.')
    hard_delete_selected.short_description = "PERMANENTLY delete selected records"
    
    # Visual indication
    def is_active_display(self, obj):
        """Show colored status indicator."""
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">●</span> Active'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">●</span> Inactive'
        )
    is_active_display.short_description = 'Status'
    is_active_display.admin_order_field = 'is_active'


class AuditAdminMixin:
    """
    Mixin for displaying audit fields (created_at, updated_at).
    """
    
    # Default fields to show in list display
    audit_list_display = ['created_at', 'updated_at', 'is_active']
    
    # Readonly audit fields
    audit_readonly_fields = ['id', 'created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        """Add audit fields to readonly."""
        readonly = list(super().get_readonly_fields(request, obj))
        return readonly + self.audit_readonly_fields


class AdemaModelAdmin(SoftDeleteAdminMixin, AuditAdminMixin, admin.ModelAdmin):
    """
    Base ModelAdmin for ADEMA models.
    
    Combines soft delete and audit mixins with sensible defaults.
    
    Example:
        @admin.register(Product)
        class ProductAdmin(AdemaModelAdmin):
            list_display = ['name', 'price', 'is_active_display', 'created_at']
            search_fields = ['name']
    """
    
    # Default list filter
    list_filter = ['is_active', 'created_at']
    
    # Default ordering
    ordering = ['-created_at']
    
    # Date hierarchy
    date_hierarchy = 'created_at'
    
    # Pagination
    list_per_page = 25
    
    # Show full result count
    show_full_result_count = True
    
    # Preserve filters
    preserve_filters = True
    
    # UUID display
    def id_short(self, obj):
        """Display shortened UUID."""
        return str(obj.id)[:8] + '...'
    id_short.short_description = 'ID'
    
    def get_fieldsets(self, request, obj=None):
        """
        Auto-generate fieldsets if not defined.
        Puts audit fields in a separate collapsible section.
        """
        fieldsets = super().get_fieldsets(request, obj)
        
        # If using default fieldsets, add audit section
        if len(fieldsets) == 1 and fieldsets[0][0] is None:
            main_fields = list(fieldsets[0][1]['fields'])
            
            # Remove audit fields from main
            audit_fields = ['id', 'created_at', 'updated_at', 'is_active']
            main_fields = [f for f in main_fields if f not in audit_fields]
            
            if main_fields:
                return [
                    (None, {'fields': main_fields}),
                    ('Audit Information', {
                        'classes': ['collapse'],
                        'fields': ['id', 'created_at', 'updated_at', 'is_active'],
                    }),
                ]
        
        return fieldsets


class TabularInlineMixin:
    """
    Mixin for tabular inlines with ADEMA defaults.
    """
    
    extra = 0
    show_change_link = True
    
    def get_readonly_fields(self, request, obj=None):
        """Make audit fields readonly in inlines."""
        readonly = list(super().get_readonly_fields(request, obj))
        return readonly + ['created_at', 'updated_at']


class StackedInlineMixin:
    """
    Mixin for stacked inlines with ADEMA defaults.
    """
    
    extra = 0
    show_change_link = True
    
    def get_readonly_fields(self, request, obj=None):
        """Make audit fields readonly in inlines."""
        readonly = list(super().get_readonly_fields(request, obj))
        return readonly + ['created_at', 'updated_at']

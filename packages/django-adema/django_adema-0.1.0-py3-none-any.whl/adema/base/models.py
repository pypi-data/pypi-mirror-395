"""
ADEMA Base Model
================

Abstract base model that provides common fields for all models:
- UUID primary key
- Audit timestamps (created_at, updated_at)
- Soft delete support (is_active)

Usage:
    from adema.base.models import AdemaBaseModel
    
    class Product(AdemaBaseModel):
        name = models.CharField(max_length=200)
        price = models.DecimalField(max_digits=10, decimal_places=2)
"""

import uuid
from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """
    Manager that filters out soft-deleted (is_active=False) records by default.
    """
    
    def get_queryset(self):
        """Return only active records."""
        return super().get_queryset().filter(is_active=True)
    
    def all_with_deleted(self):
        """Return all records including soft-deleted ones."""
        return super().get_queryset()
    
    def deleted_only(self):
        """Return only soft-deleted records."""
        return super().get_queryset().filter(is_active=False)


class AllObjectsManager(models.Manager):
    """
    Manager that returns all objects regardless of is_active status.
    Use this when you need to access soft-deleted records.
    """
    pass


class AdemaBaseModel(models.Model):
    """
    Abstract base model for all ADEMA models.
    
    Provides:
        - id: UUID primary key (more secure and suitable for distributed systems)
        - created_at: Timestamp when the record was created
        - updated_at: Timestamp when the record was last modified
        - is_active: Soft delete flag (False = deleted)
    
    Example:
        class Customer(AdemaBaseModel):
            name = models.CharField(max_length=200)
            email = models.EmailField(unique=True)
            
            class Meta:
                verbose_name = 'Customer'
                verbose_name_plural = 'Customers'
    """
    
    # UUID as primary key - better for distributed systems and API security
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID',
        help_text='Unique identifier for this record'
    )
    
    # Audit timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
        help_text='Date and time when this record was created'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At',
        help_text='Date and time when this record was last modified'
    )
    
    # Soft delete support
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
        help_text='Designates whether this record should be treated as active. '
                  'Unselect this instead of deleting records.'
    )
    
    # Managers
    objects = SoftDeleteManager()  # Default manager - returns only active
    all_objects = AllObjectsManager()  # Returns all including deleted
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
        get_latest_by = 'created_at'
    
    def soft_delete(self):
        """
        Soft delete this record by setting is_active to False.
        
        Example:
            product.soft_delete()
        """
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])
    
    def restore(self):
        """
        Restore a soft-deleted record by setting is_active to True.
        
        Example:
            product.restore()
        """
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])
    
    def hard_delete(self):
        """
        Permanently delete this record from the database.
        Use with caution - this cannot be undone.
        
        Example:
            product.hard_delete()
        """
        super().delete()
    
    @classmethod
    def get_by_id(cls, id):
        """
        Get a record by its UUID.
        
        Args:
            id: UUID string or UUID object
            
        Returns:
            The record or None if not found
            
        Example:
            product = Product.get_by_id('123e4567-e89b-12d3-a456-426614174000')
        """
        try:
            return cls.objects.get(id=id)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_or_none(cls, **kwargs):
        """
        Get a single record matching the criteria or None.
        
        Args:
            **kwargs: Filter criteria
            
        Returns:
            The record or None if not found
            
        Example:
            customer = Customer.get_or_none(email='test@example.com')
        """
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned:
            return cls.objects.filter(**kwargs).first()


class TimeStampedModel(models.Model):
    """
    Abstract model with only timestamp fields (no UUID, no soft delete).
    Use when you need simpler audit tracking.
    """
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class NamedModel(AdemaBaseModel):
    """
    Abstract model with a name field.
    Useful for simple lookup tables and catalogs.
    """
    
    name = models.CharField(
        max_length=200,
        verbose_name='Name',
        help_text='Display name for this record'
    )
    
    class Meta:
        abstract = True
        ordering = ['name']
    
    def __str__(self):
        return self.name


class OrderedModel(AdemaBaseModel):
    """
    Abstract model with ordering support.
    Useful for items that need manual ordering (menus, steps, etc.)
    """
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Order',
        help_text='Display order (lower numbers appear first)'
    )
    
    class Meta:
        abstract = True
        ordering = ['order', '-created_at']
    
    def move_up(self):
        """Move this item up in the order."""
        if self.order > 0:
            self.order -= 1
            self.save(update_fields=['order'])
    
    def move_down(self):
        """Move this item down in the order."""
        self.order += 1
        self.save(update_fields=['order'])

"""
ADEMA Base Service
==================

Base service class with integrated logging and transaction support.
Services contain business logic separated from views.

Usage:
    from adema.base.services import AdemaBaseService
    
    class OrderService(AdemaBaseService):
        def create_order(self, customer_id, items):
            with self.transaction():
                self.log.info(f"Creating order for customer {customer_id}")
                # Business logic here
"""

import logging
import functools
from typing import Any, Callable, Optional, TypeVar, Generic
from contextlib import contextmanager

from django.db import transaction


T = TypeVar('T')


class ServiceResult(Generic[T]):
    """
    Wrapper for service method results.
    Provides a consistent way to return success/failure with data.
    
    Example:
        def get_customer(self, id):
            customer = Customer.get_by_id(id)
            if customer:
                return ServiceResult.success(customer)
            return ServiceResult.failure("Customer not found")
    """
    
    def __init__(
        self,
        success: bool,
        data: Optional[T] = None,
        message: str = "",
        errors: Optional[list] = None
    ):
        self.success = success
        self.data = data
        self.message = message
        self.errors = errors or []
    
    @classmethod
    def ok(cls, data: T = None, message: str = "") -> 'ServiceResult[T]':
        """Create a successful result."""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def fail(cls, message: str, errors: list = None) -> 'ServiceResult[T]':
        """Create a failure result."""
        return cls(success=False, message=message, errors=errors)
    
    # Aliases
    success = ok
    failure = fail
    
    def __bool__(self):
        """Allow using result in if statements."""
        return self.success
    
    def to_dict(self) -> dict:
        """Convert to dictionary (useful for API responses)."""
        result = {
            'success': self.success,
            'message': self.message,
        }
        if self.data is not None:
            result['data'] = self.data
        if self.errors:
            result['errors'] = self.errors
        return result


class AdemaBaseService:
    """
    Base class for all service classes in ADEMA projects.
    
    Provides:
        - Integrated logging with self.log
        - Transaction management with self.transaction()
        - Standard result wrapping with ServiceResult
    
    Example:
        class ProductService(AdemaBaseService):
            def __init__(self):
                super().__init__()
                # Additional initialization
            
            def create_product(self, name, price):
                with self.transaction():
                    self.log.info(f"Creating product: {name}")
                    product = Product.objects.create(name=name, price=price)
                    self.log.info(f"Product created with ID: {product.id}")
                    return ServiceResult.ok(product)
    """
    
    def __init__(self):
        """Initialize the service with a logger."""
        self.log = logging.getLogger(self.__class__.__name__)
    
    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions.
        
        Automatically commits on success and rolls back on exception.
        
        Example:
            with self.transaction():
                order.status = 'confirmed'
                order.save()
                self.create_invoice(order)  # Rolls back if this fails
        """
        try:
            with transaction.atomic():
                yield
        except Exception as e:
            self.log.error(f"Transaction failed: {e}")
            raise
    
    def atomic(self, func: Callable) -> Callable:
        """
        Decorator to wrap a method in a database transaction.
        
        Example:
            @self.atomic
            def process_order(self, order):
                # Everything here runs in a transaction
                pass
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self.transaction():
                return func(*args, **kwargs)
        return wrapper


def transactional(func: Callable) -> Callable:
    """
    Decorator to wrap any function in a database transaction.
    Can be used on service methods or standalone functions.
    
    Example:
        @transactional
        def bulk_update_prices(products, new_price):
            for product in products:
                product.price = new_price
                product.save()
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with transaction.atomic():
            return func(*args, **kwargs)
    return wrapper


def log_method(func: Callable) -> Callable:
    """
    Decorator to automatically log method entry/exit and exceptions.
    
    Example:
        @log_method
        def calculate_total(self, items):
            # Will log: "Entering calculate_total"
            # Will log: "Exiting calculate_total" or exception details
            return sum(item.price for item in items)
    """
    logger = logging.getLogger(func.__module__)
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting {func.__name__}")
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__name__}: {e}")
            raise
    
    return wrapper


class CRUDService(AdemaBaseService):
    """
    Base service with standard CRUD operations.
    
    Subclass and set model_class to get basic CRUD functionality.
    
    Example:
        class ProductService(CRUDService):
            model_class = Product
        
        service = ProductService()
        product = service.create(name="Widget", price=9.99)
        products = service.list(is_active=True)
    """
    
    model_class = None
    
    def get(self, id) -> ServiceResult:
        """
        Get a single record by ID.
        
        Args:
            id: The record ID (UUID)
            
        Returns:
            ServiceResult with the record or failure message
        """
        if not self.model_class:
            return ServiceResult.fail("model_class not set")
        
        record = self.model_class.get_by_id(id)
        if record:
            return ServiceResult.ok(record)
        return ServiceResult.fail(f"{self.model_class.__name__} not found")
    
    def list(self, **filters) -> ServiceResult:
        """
        List records with optional filters.
        
        Args:
            **filters: Django ORM filter kwargs
            
        Returns:
            ServiceResult with queryset
        """
        if not self.model_class:
            return ServiceResult.fail("model_class not set")
        
        queryset = self.model_class.objects.filter(**filters)
        return ServiceResult.ok(queryset)
    
    def create(self, **data) -> ServiceResult:
        """
        Create a new record.
        
        Args:
            **data: Field values for the new record
            
        Returns:
            ServiceResult with the created record
        """
        if not self.model_class:
            return ServiceResult.fail("model_class not set")
        
        try:
            with self.transaction():
                record = self.model_class.objects.create(**data)
                self.log.info(f"Created {self.model_class.__name__} with ID: {record.id}")
                return ServiceResult.ok(record, "Created successfully")
        except Exception as e:
            self.log.error(f"Failed to create {self.model_class.__name__}: {e}")
            return ServiceResult.fail(str(e))
    
    def update(self, id, **data) -> ServiceResult:
        """
        Update an existing record.
        
        Args:
            id: The record ID
            **data: Field values to update
            
        Returns:
            ServiceResult with the updated record
        """
        if not self.model_class:
            return ServiceResult.fail("model_class not set")
        
        record = self.model_class.get_by_id(id)
        if not record:
            return ServiceResult.fail(f"{self.model_class.__name__} not found")
        
        try:
            with self.transaction():
                for key, value in data.items():
                    setattr(record, key, value)
                record.save()
                self.log.info(f"Updated {self.model_class.__name__} {id}")
                return ServiceResult.ok(record, "Updated successfully")
        except Exception as e:
            self.log.error(f"Failed to update {self.model_class.__name__}: {e}")
            return ServiceResult.fail(str(e))
    
    def delete(self, id, hard: bool = False) -> ServiceResult:
        """
        Delete a record (soft delete by default).
        
        Args:
            id: The record ID
            hard: If True, permanently delete. If False, soft delete.
            
        Returns:
            ServiceResult with success/failure
        """
        if not self.model_class:
            return ServiceResult.fail("model_class not set")
        
        # Use all_objects to find even soft-deleted records for hard delete
        manager = self.model_class.all_objects if hard else self.model_class.objects
        
        try:
            record = manager.get(id=id)
        except self.model_class.DoesNotExist:
            return ServiceResult.fail(f"{self.model_class.__name__} not found")
        
        try:
            with self.transaction():
                if hard:
                    record.hard_delete()
                    self.log.info(f"Hard deleted {self.model_class.__name__} {id}")
                else:
                    record.soft_delete()
                    self.log.info(f"Soft deleted {self.model_class.__name__} {id}")
                return ServiceResult.ok(message="Deleted successfully")
        except Exception as e:
            self.log.error(f"Failed to delete {self.model_class.__name__}: {e}")
            return ServiceResult.fail(str(e))

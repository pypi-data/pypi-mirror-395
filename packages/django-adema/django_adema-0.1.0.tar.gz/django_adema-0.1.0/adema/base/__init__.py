"""
ADEMA Base Module
=================

Core library components that are installed in site-packages
and can be imported by generated projects.
"""

from adema.base.models import AdemaBaseModel
from adema.base.services import AdemaBaseService
from adema.base.apps import AdemaAppConfig

__all__ = ['AdemaBaseModel', 'AdemaBaseService', 'AdemaAppConfig']

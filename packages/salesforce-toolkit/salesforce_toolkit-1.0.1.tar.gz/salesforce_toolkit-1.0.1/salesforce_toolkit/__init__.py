"""
Salesforce Toolkit - A comprehensive Python library for Salesforce integration.

This toolkit provides a flexible, configuration-driven framework for:
- Authentication (JWT Bearer Flow, OAuth Password Flow)
- CRUD operations on any Salesforce object
- Field mapping and data transformation
- ETL pipelines for data synchronization
- Comprehensive logging and error handling

Author: Antonio Trento
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Antonio Trento"

from salesforce_toolkit.auth.jwt_auth import JWTAuthenticator
from salesforce_toolkit.auth.oauth_auth import OAuthAuthenticator
from salesforce_toolkit.core.session import SalesforceSession
from salesforce_toolkit.core.client import SalesforceClient
from salesforce_toolkit.mapping.field_mapper import FieldMapper
from salesforce_toolkit.pipeline.sync_pipeline import SyncPipeline, SyncMode

__all__ = [
    "JWTAuthenticator",
    "OAuthAuthenticator",
    "SalesforceSession",
    "SalesforceClient",
    "FieldMapper",
    "SyncPipeline",
    "SyncMode",
]

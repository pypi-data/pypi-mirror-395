"""
Pipeline module for Salesforce Toolkit.

Provides ETL pipeline framework for data synchronization.
"""

from salesforce_toolkit.pipeline.sync_pipeline import (
    SyncPipeline,
    SyncMode,
    SyncStatus,
    SyncResult
)

__all__ = ["SyncPipeline", "SyncMode", "SyncStatus", "SyncResult"]

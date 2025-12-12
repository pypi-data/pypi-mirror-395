"""Migration 0003 re-export - Python modules cannot start with numbers."""

import importlib

_module = importlib.import_module("api.database.migrations.0003_resource_deduplication_and_checkpoints")
Migration0003ResourceDeduplicationAndCheckpoints = _module.Migration0003ResourceDeduplicationAndCheckpoints

__all__ = ["Migration0003ResourceDeduplicationAndCheckpoints"]


"""Migration 0006 re-export - Python modules cannot start with numbers."""

import importlib

_module = importlib.import_module("api.database.migrations.0006_predictive_cache")
Migration0006PredictiveCache = _module.Migration0006PredictiveCache

__all__ = ["Migration0006PredictiveCache"]


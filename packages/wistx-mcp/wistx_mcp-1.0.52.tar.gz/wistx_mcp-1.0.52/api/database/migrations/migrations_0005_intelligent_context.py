"""Migration 0005 re-export - Python modules cannot start with numbers."""

import importlib

_module = importlib.import_module("api.database.migrations.0005_intelligent_context")
Migration0005IntelligentContext = _module.Migration0005IntelligentContext

__all__ = ["Migration0005IntelligentContext"]


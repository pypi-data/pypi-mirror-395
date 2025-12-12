"""Migration 0004 re-export - Python modules cannot start with numbers."""

import importlib

_module = importlib.import_module("api.database.migrations.0004_virtual_filesystem")
Migration0004VirtualFilesystem = _module.Migration0004VirtualFilesystem

__all__ = ["Migration0004VirtualFilesystem"]


"""
Backward compatibility module for langgraph_api.
This module provides an alias to orcakit_api for backward compatibility.
All imports from langgraph_api will be redirected to orcakit_api.

DEPRECATED: Please use orcakit_api instead.
"""
import sys
import importlib

# Dynamically import all content from orcakit_api
orcakit_api = importlib.import_module('orcakit_api')

# Replace this module in sys.modules with orcakit_api
sys.modules['langgraph_api'] = orcakit_api

# Export all public interfaces
__all__ = orcakit_api.__all__ if hasattr(orcakit_api, '__all__') else []

# Export all attributes from orcakit_api
for attr in dir(orcakit_api):
    if not attr.startswith('_'):
        globals()[attr] = getattr(orcakit_api, attr)

# Export version for compatibility
__version__ = orcakit_api.__version__

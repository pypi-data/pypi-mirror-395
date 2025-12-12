"""
DNV HydroD Python Package

This package provides Python utilities for working with DNV HydroD workspaces.
It handles .NET assembly loading, workspace session management, and provides
access to HydroD modeling APIs through pythonnet.

Main components:
- load_assemblies: Initializes .NET runtime and loads HydroD assemblies
- workspace_utils: Provides WorkspaceSession context manager for workspace operations
- Embedded Python modules: Custom utilities loaded from HydroD .NET assemblies

Features:
- Automatic HydroD installation detection via DNV Application Version Manager
- Context manager for safe workspace session handling
- Access to HydroD modeling APIs (concepts, analyses, etc.)
- Support for both opening existing and creating new workspaces

Usage:
    >>> from dnv.hydrod import *
    >>> 
    >>> # Open existing workspace
    >>> with WorkspaceSession(r"C:\Projects\myworkspace.hydx", license_keys=['HydroD', 'WIND']) as session:
    ...     # Access workspace concepts
    ...     analyses = FindConcept("/Workspace/Analyses")
    ...     
    ...     # Create custom analysis
    ...     ca = CustomAnalysis(analyses, "MyAnalysis")
    ...     ca.InlineScript = "print('Hello from HydroD')"
    ...     ca.Execute()

Requirements:
- DNV HydroD 8.1 and higher (must be installed on the system)
- Python 3.10, 3.11, 3.12, or 3.13 (3.14+ not supported)
"""

from .workspace_utils import *

__version__ = "1.0.0"
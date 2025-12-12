"""
HydroD Assembly Loader

This module provides utilities for loading HydroD .NET assemblies and embedded Python modules
into the Python runtime using pythonnet. It handles:
- Locating the HydroD application installation
- Loading required .NET assemblies from configuration
- Extracting and executing embedded Python modules from .NET assemblies
"""

import json
import os
from typing import Dict, Any, Optional
from pythonnet import load

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSEMBLY_DIR = os.path.join(SCRIPT_DIR, '.dlls')
RUNTIME_CONFIG = os.path.join(SCRIPT_DIR, 'runtimeconfig.json')
PYTHON_SCRIPT_CONFIG = 'PythonScriptConfig.json'
PYTHON_HELPERS_ASSEMBLY = 'DNV.Sigma.ApplicationCore.PythonHelpers'
APP_VERSION_MANAGER_DLL = 'DNV.ApplicationVersionManager.Core.dll'

# Initialize .NET Core runtime
load("coreclr", runtime_config=RUNTIME_CONFIG)

import clr
from System import Reflection

# Dictionary to store dynamically loaded symbols from embedded modules
_embedded_symbols: Dict[str, Any] = {}

# Cache for HydroD path to avoid expensive lookups
_hydrod_path_cache: Optional[str] = None


def load_assemblies(hydrod_libraries_path: str) -> None:
    """
    Load required .NET assemblies for HydroD from configuration file.

    Args:
        hydrod_libraries_path: Path to the HydroD libraries directory containing DLL files.

    Raises:
        RuntimeError: If assembly loading fails or configuration file is invalid.
    """
    # Add native DLL directories to PATH for .NET Core runtime dependencies
    # This is required for native libraries like lsapiw64.dll (Thales licensing)
    import platform
    arch = 'win-x64' if platform.architecture()[0] == '64bit' else 'win-x86'
    native_dll_path = os.path.join(hydrod_libraries_path, 'runtimes', arch, 'native')
    
    if os.path.exists(native_dll_path):
        # Prepend to PATH to ensure these DLLs are found first
        os.environ['PATH'] = native_dll_path + os.pathsep + os.environ.get('PATH', '')
    
    config_path = os.path.join(hydrod_libraries_path, PYTHON_SCRIPT_CONFIG)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            dll_config = json.load(file)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in configuration file: {e}")

    try:
        for dll in dll_config.get('dlls', []):
            dll_name = dll.get('name')
            if not dll_name:
                continue
                
            dll_path = os.path.join(hydrod_libraries_path, dll_name)
            
            # Native DLLs require LoadFile, managed DLLs use AddReference
            if dll.get('isNative', False):
                Reflection.Assembly.LoadFile(dll_path)
            else:
                clr.AddReference(dll_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load HydroD assemblies: {e}")


def get_hydrod_path() -> str:
    """
    Locate the HydroD application installation path.

    Uses the DNV Application Version Manager to find the default HydroD installation
    and returns the directory containing the executable and DLL files.
    
    The result is cached after the first call to avoid expensive lookups.

    Returns:
        str: Absolute path to the HydroD libraries directory.

    Raises:
        RuntimeError: If HydroD application is not found or not installed.
    """
    global _hydrod_path_cache
    
    # Return cached value if already computed
    if _hydrod_path_cache is not None:
        return _hydrod_path_cache
    
    app_version_manager_path = os.path.join(ASSEMBLY_DIR, APP_VERSION_MANAGER_DLL)
    
    try:
        clr.AddReference(app_version_manager_path)
        from DNV.ApplicationVersionManager.Core import AppVersionServiceLocator
    except Exception as e:
        raise RuntimeError(f"Failed to load Application Version Manager: {e}")

    try:
        hydrod_app = AppVersionServiceLocator.Default.AppVersionSearcher.GetDefaultApplication('HydroD')
        
        if hydrod_app is None:
            raise RuntimeError(
                "HydroD application not found. Please ensure HydroD is installed on this system."
            )

        _hydrod_path_cache = os.path.dirname(os.path.abspath(hydrod_app.ExeFilePath))
        return _hydrod_path_cache
    except Exception as e:
        raise RuntimeError(f"Failed to locate HydroD application: {e}")


def load_embedded_python_modules(hydrod_libraries_path: str) -> None:
    """
    Extract and execute Python modules embedded in .NET assemblies.

    Loads the PythonHelpers assembly, extracts embedded .py files from its resources,
    and executes them in the current Python environment.

    Args:
        hydrod_libraries_path: Path to the HydroD libraries directory.

    Raises:
        RuntimeError: If the assembly cannot be loaded or Python modules cannot be executed.
    """
    from System.IO import StreamReader
    from System.Reflection import Assembly

    assembly_path = os.path.join(hydrod_libraries_path, f'{PYTHON_HELPERS_ASSEMBLY}.dll')
    
    try:
        clr.AddReference(assembly_path)
        assembly = Assembly.Load(PYTHON_HELPERS_ASSEMBLY)
    except Exception as e:
        raise RuntimeError(f"Failed to load {PYTHON_HELPERS_ASSEMBLY}: {e}")

    resource_names = assembly.GetManifestResourceNames()

    for resource_name in resource_names:
        # Case-insensitive check for .py extension
        if not resource_name.lower().endswith('.py'):
            continue
        
        # Skip InternalPython resources
        if 'InternalPython'.lower() in resource_name.lower():
            continue

        stream = assembly.GetManifestResourceStream(resource_name)
        if stream is None:
            continue

        try:
            reader = StreamReader(stream)
            code = reader.ReadToEnd()
            reader.Close()
            
            # Capture globals before execution to track new symbols
            globals_before = set(globals().keys())
            
            # Execute the embedded Python code in the module's global namespace
            # This ensures functions can reference each other and module globals
            module_globals = globals()
            exec(code, module_globals, module_globals)
            
            # Track which symbols were added
            globals_after = set(globals().keys())
            new_symbols = globals_after - globals_before
            
            # Add new symbols to _embedded_symbols
            for name in new_symbols:
                if not name.startswith('_'):
                    _embedded_symbols[name] = globals()[name]
            
        except Exception as e:
            raise RuntimeError(f"Failed to execute embedded module '{resource_name}': {e}")


def initialize_hydrod() -> str:
    """
    Initialize HydroD environment by loading all required assemblies and modules.

    This is the main entry point that orchestrates the complete initialization process:
    1. Locates HydroD installation
    2. Loads .NET assemblies
    3. Loads embedded Python modules

    Returns:
        str: Path to the HydroD libraries directory.

    Raises:
        RuntimeError: If any initialization step fails.
    """
    hydrod_libraries = get_hydrod_path()
    load_assemblies(hydrod_libraries)
    load_embedded_python_modules(hydrod_libraries)
    return hydrod_libraries


def get_embedded_symbols() -> Dict[str, Any]:
    """
    Get all symbols loaded from embedded Python modules.
    
    Returns:
        Dictionary of symbol names to values from embedded modules.
    """
    return _embedded_symbols.copy()


def clear_hydrod_path_cache() -> None:
    """
    Clear the cached HydroD path.
    
    Forces the next call to get_hydrod_path() to perform a fresh lookup.
    Useful if HydroD installation path changes during runtime.
    """
    global _hydrod_path_cache
    _hydrod_path_cache = None


# Auto-initialize when module is imported
if __name__ != '__main__':
    initialize_hydrod()
    
    # Make embedded symbols available for 'from load_assemblies import *'
    __all__ = ['load_assemblies', 'get_hydrod_path', 'load_embedded_python_modules', 
               'initialize_hydrod', 'get_embedded_symbols', 'clear_hydrod_path_cache'] + list(_embedded_symbols.keys())
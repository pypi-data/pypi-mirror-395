"""
DNV HydroD Workspace Utilities

This module provides utilities for working with HydroD workspaces in Python.
It handles workspace session management and provides access to HydroD modeling APIs.

The module automatically loads required .NET assemblies and imports HydroD namespaces
when imported. All imported symbols are available for use in workspace operations.
"""

from typing import Optional
from . import load_assemblies as _load_assemblies_module

# Import all embedded symbols from load_assemblies (e.g., FindConcept, CustomAnalysis, etc.)
from .load_assemblies import *

# Import HydroD .NET namespaces
# These imports become available after load_assemblies initializes the .NET runtime
from DNVS.HydroD.Environment import *
from DNVS.HydroD.HydroModeling import *
from DNVS.HydroD.Analysis import *
from DNVS.Commons.ModelCore import *
from DNVS.Sesam.Commons.ConceptCore import *
from DNV.SesamX.SesamWorkflows.Concepts import *
from DNV.SesamX.SesamWorkflows.Enums import *

from HydroD.SessionHost import WorkspaceSession as _WorkspaceSessionImpl
from DNVS.Sesam.Commons.ApplicationCore import QuantityProvider

# Module-level globals for workspace session state
__workspace_session__: Optional[_WorkspaceSessionImpl] = None
__quantity_provider__: Optional[QuantityProvider] = None

# Make workspace session accessible to embedded modules in load_assemblies
# This allows get_workspace() and get_workspace_service() to find the session
_load_assemblies_module.__workspace_session__ = __workspace_session__
_load_assemblies_module.__quantity_provider__ = __quantity_provider__

class WorkspaceSession:
    r"""
    Context manager for HydroD workspace sessions.
    
    Provides a Pythonic interface for opening or creating HydroD workspace files. 
    Automatically saves workspace on exit when used as a context manager.
    
    Example:
        >>> # Open existing workspace
        >>> with WorkspaceSession(r"C:\Projects\myworkspace.hydx") as session:
        ...     # Work with workspace
        ...     pass
        
        >>> # Create new workspace
        >>> with WorkspaceSession(r"C:\Projects", "NewWorkspace") as session:
        ...     # Work with new workspace (saved as NewWorkspace.hydx)
        ...     pass
    
    Attributes:
        session: The underlying HydroD workspace session object.
    """

    def __init__(
        self, 
        path_or_directory: str,
        workspace_name: Optional[str] = None,
        template_path: Optional[str] = None,
        save_on_exit: bool = True,
        license_keys: Optional[list[str]] = None
    ):
        r"""
        Initialize a workspace session by either opening existing or creating new workspace.

        Args:
            path_or_directory: If workspace_name is None, this is the path to existing 
                             workspace file (.hydx) to open. If workspace_name is provided,
                             this is the directory where new workspace will be created.
            workspace_name: Name of new workspace (without .hydx extension). 
                          If provided, creates new workspace in path_or_directory.
                          If None, opens existing workspace from path_or_directory.
            template_path: Path to workspace template file (.hydt) to use when creating
                         new workspace. If None, uses default HydroD template.
                         Only used when workspace_name is provided.
            save_on_exit: Whether to automatically save workspace when exiting context manager.
                        Defaults to True.
            license_keys: Optional list of license keys to use for this session.
                        If None, uses default licensing.

        Raises:
            RuntimeError: If workspace cannot be opened or created.
            
        Examples:
            >>> # Open existing workspace (1 argument)
            >>> session = WorkspaceSession(r"C:\Projects\existing.hydx")
            
            >>> # Create new workspace with default template (2 arguments)
            >>> session = WorkspaceSession(r"C:\Projects", "NewWorkspace")
            
            >>> # Create new workspace with custom template (3 arguments)
            >>> session = WorkspaceSession(r"C:\Projects", "NewWorkspace", r"C:\Templates\custom.hydt")
            
            >>> # Open without auto-save and with license keys
            >>> session = WorkspaceSession(r"C:\Projects\existing.hydx", save_on_exit=False, license_keys=["KEY1", "KEY2"])
        """
        global __workspace_session__, __quantity_provider__
        
        # Convert Python list to .NET array if license_keys provided
        license_keys_array = None
        if license_keys is not None:
            from System import Array, String
            license_keys_array = Array[String](license_keys)
        
        try:
            __workspace_session__ = _WorkspaceSessionImpl(
                saveWorkspaceOnExit=save_on_exit,
                licenseKeys=license_keys_array
            )
            __quantity_provider__ = QuantityProvider()
        except Exception as e:
            from System import InvalidOperationException
            if isinstance(e, InvalidOperationException):
                # Detect if running in Jupyter/IPython
                try:
                    get_ipython()
                    is_jupyter = True
                except NameError:
                    is_jupyter = False
                
                if is_jupyter:
                    import sys
                    sys.exit(1)
                else:
                    # In scripts, exit cleanly without pythonnet cleanup issues
                    import os
                    os._exit(1)
            raise RuntimeError(
                f"Failed to initialize HydroD workspace session: {e}"
            ) from e
        
        # Sync with load_assemblies module so embedded functions can access it
        _load_assemblies_module.__workspace_session__ = __workspace_session__
        _load_assemblies_module.__quantity_provider__ = __quantity_provider__
        
        self.session = __workspace_session__
        
        # Decide based on number of arguments: 1 = open, 2+ = create
        if workspace_name is None:
            # Single argument: open existing workspace
            self.session.OpenWorkspace(path_or_directory)
        else:
            # Two or three arguments: create new workspace
            import os
            from .load_assemblies import get_hydrod_path
            
            # Use provided template or default from HydroD installation
            if template_path is None:
                hydrod_path = get_hydrod_path()
                template_path = os.path.join(hydrod_path, 'Templates', 'Default.hydt')
            
            self.session.CreateWorkspace(path_or_directory, workspace_name, template_path)
        

    def __enter__(self) -> 'WorkspaceSession':
        """
        Enter the context manager.

        Returns:
            Self for use in with statements.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the context manager and clean up resources.

        Disposes of the workspace session, ensuring proper cleanup and saving
        if configured to do so.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.
        """
        if self.session:
            self.session.Dispose()
            # Clear references in load_assemblies module
            _load_assemblies_module.__workspace_session__ = None
            _load_assemblies_module.__quantity_provider__ = None
    
    def close(self) -> None:
        """
        Explicitly close the workspace session.
        
        Useful when not using the context manager pattern.
        """
        if self.session:
            self.session.Dispose()
            # Clear references in load_assemblies module
            _load_assemblies_module.__workspace_session__ = None
            _load_assemblies_module.__quantity_provider__ = None


def get_workspace_session() -> Optional[_WorkspaceSessionImpl]:
    """
    Get the current active workspace session.

    Returns:
        The active workspace session, or None if no session is active.
    """
    return __workspace_session__


def get_quantity_provider() -> Optional[QuantityProvider]:
    """
    Get the current quantity provider instance.

    Returns:
        The active quantity provider, or None if not initialized.
    """
    return __quantity_provider__


# Export all symbols: workspace utilities + embedded symbols + .NET imports
_embedded = _load_assemblies_module.get_embedded_symbols()

# Collect all .NET symbols imported via namespace imports
_dotnet_symbols = [
    name for name in dir() 
    if not name.startswith('_') 
    and name not in ['Optional', 'typing', 'load_assemblies']  # Exclude Python imports
]

__all__ = [
    # Workspace utilities
    'WorkspaceSession',
    'get_workspace_session', 
    'get_quantity_provider',
    '__workspace_session__',
    '__quantity_provider__',
] + list(_embedded.keys()) + _dotnet_symbols
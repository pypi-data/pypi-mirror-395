# dnv-hydrod

dnv-hydrod is a Python library that provides seamless integration with DNV HydroD through pythonnet, enabling programmatic access to HydroD workspace files (.hydx) and modeling APIs.

This library automatically locates your HydroD installation, loads required .NET assemblies, and provides a Pythonic interface for workspace operations, analysis execution, and concept manipulation.

**Requirements:** 
- DNV HydroD 9.0 and higher (must be installed on the system)
- Python 3.10, 3.11, 3.12, or 3.13 (3.14+ not supported)

## Installation

Installing from PyPI (when published):

```bash
pip install dnv-hydrod
```

## Quick Start

```python
from dnv.hydrod import *

# Open existing workspace with license keys
with WorkspaceSession(
    r"C:\Projects\myworkspace.hydx",
    license_keys=['WIND']
) as session:
    # Access workspace concepts
    analyses = FindConcept("/Workspace/Analyses")
    
    # Create and execute custom analysis
    ca = CustomAnalysis(analyses, "MyAnalysis")
    ca.InlineScript = """
import time
print('Starting analysis...')
time.sleep(2)
print('Analysis completed!')
"""
    ca.Execute()
```

## Key Features

- **Automatic HydroD Detection**: Uses DNV Application Version Manager to locate HydroD installation
- **Context Manager Support**: Safe workspace handling with automatic cleanup
- **Pythonic API**: Clean, intuitive interface for HydroD operations
- **Embedded Modules**: Access to Python utilities embedded in HydroD .NET assemblies

## Documentation

This library provides Python bindings to HydroD's .NET API. For comprehensive information about available classes, methods, workflows, and HydroD concepts, please refer to the **HydroD Documentation** and API reference included with your HydroD installation.

## Usage Examples

### Creating a New Workspace

```python
from dnv.hydrod import *

# Create new workspace with license keys
with WorkspaceSession(
    r"C:\Projects",
    "NewWorkspace",
    license_keys=['WIND']
) as session:
    # Workspace is automatically saved as NewWorkspace.hydx
    print("Workspace created successfully!")
```

### Working with Concepts

```python
from dnv.hydrod import *

with WorkspaceSession(
    r"C:\Projects\myworkspace.hydx",
    license_keys=['WIND']
) as session:
    # Find concepts using path
    load_cases_table = FindConcept("/Workspace/Analyses/DesignLoadCasesTable1")

    # Create new DesignLoadCase entry
    udlc1 = DesignLoadCase()
    udlc1.Selected=True
    udlc1.Name="DLC_new"
    udlc1.SimaBladedFolder="Inputs\\Sima_ULS_Hs11_Deg90_Vw23"
    udlc1.SimaBladedFileName="sima"
    udlc1.EnvironmentalLoadFactor=0.8
    udlc1.PermanentLoadFactor=0.8
    udlc1.StartTime=300
    udlc1.StopTime=340

    # Add new DesignLoadCase entry to "UlsDesignLoadCases1" concept
    load_cases_table.DesignLoadCases.Add(udlc1)
```

### Generate Runs and run ULS workflow through Python

```python
from dnv.hydrod import *

with WorkspaceSession(
    r"C:\Projects\myworkspace.hydx",
    license_keys=['WIND']
) as session:
    runFolder = FindConcept("/Workspace/Analyses/Workflow1/Runs")
    # If the run folder already exists, delete it to remove previous results
    if (runFolder):
        Delete(runFolder)

    workflow = FindConcept("/Workspace/Analyses/Workflow1")
    workflow.GenerateRuns()
    workflow.Execute()
```

## Architecture

- **load_assemblies.py**: Initializes .NET runtime, locates HydroD, loads assemblies
- **workspace_utils.py**: Provides WorkspaceSession and utility functions
- **Embedded modules**: Python code extracted from HydroD .NET assemblies at runtime

## Limitations

- HydroD must be installed on the system

## License

This project is licensed under the MIT License. See the LICENSE file in the package directory for full license text.

## Support

For issues, questions, or feedback, please contact DNV software support at software.support@dnv.com.

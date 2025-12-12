"""
PyImport2Pkg: Reverse mapping from Python imports to pip package names.

A tool for the AI-assisted coding era that helps developers quickly identify
which pip packages need to be installed based on import statements in code.
"""

__version__ = "0.3.0"

from .models import (
    ImportType,
    ImportContext,
    ImportInfo,
    PackageCandidate,
    MappingResult,
    AnalysisResult,
)

__all__ = [
    "__version__",
    "ImportType",
    "ImportContext",
    "ImportInfo",
    "PackageCandidate",
    "MappingResult",
    "AnalysisResult",
]

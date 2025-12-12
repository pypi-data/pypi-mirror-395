"""
PyImport2Pkg: Reverse mapping from Python imports to pip package names.

A tool for the AI-assisted coding era that helps developers quickly identify
which pip packages need to be installed based on import statements in code.
"""

__version__ = "1.0.0"

from .models import (
    ImportType,
    ImportContext,
    ImportInfo,
    PackageCandidate,
    MappingResult,
    AnalysisResult,
)

from .scanner import Scanner, scan_project
from .parser import Parser
from .filter import Filter
from .mapper import Mapper
from .resolver import Resolver, ResolveStrategy
from .exporter import Exporter

__all__ = [
    "__version__",
    # Models
    "ImportType",
    "ImportContext",
    "ImportInfo",
    "PackageCandidate",
    "MappingResult",
    "AnalysisResult",
    # Core classes
    "Scanner",
    "scan_project",
    "Parser",
    "Filter",
    "Mapper",
    "Resolver",
    "ResolveStrategy",
    "Exporter",
]

"""
Scientific API connectors for research workflows.

This module provides specialized connectors for common scientific APIs
used in research, including bioinformatics, academic publications,
citation data, chemical compounds, and researcher profiles.
"""

from .ncbi import NCBIConnector
from .arxiv import ArXivConnector
from .crossref import CrossRefConnector
from .semantic_scholar import SemanticScholarConnector
from .pubchem import PubChemConnector
from .orcid import ORCIDConnector

__all__ = [
    "NCBIConnector",
    "ArXivConnector",
    "CrossRefConnector",
    "SemanticScholarConnector",
    "PubChemConnector",
    "ORCIDConnector",
]

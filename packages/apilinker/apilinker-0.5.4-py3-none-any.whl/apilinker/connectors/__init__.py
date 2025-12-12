"""
API connectors for various services and platforms.

This package contains specialized connectors for different types of APIs,
including scientific research APIs, general-purpose APIs, and more.
"""

# Import connectors from subpackages
from .scientific import (
    NCBIConnector,
    ArXivConnector,
    CrossRefConnector,
    SemanticScholarConnector,
    PubChemConnector,
    ORCIDConnector,
)

from .general import (
    GitHubConnector,
    NASAConnector,
)

__all__ = [
    # Scientific connectors
    "NCBIConnector",
    "ArXivConnector",
    "CrossRefConnector",
    "SemanticScholarConnector",
    "PubChemConnector",
    "ORCIDConnector",
    # General connectors
    "GitHubConnector",
    "NASAConnector",
]

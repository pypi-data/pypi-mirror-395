"""
NCBI (National Center for Biotechnology Information) API connector.

Provides access to NCBI's Entrez API for biomedical and genomic data,
including PubMed, GenBank, and other databases.
"""

from typing import Any, Dict, List, Optional
from apilinker.core.connector import ApiConnector


class NCBIConnector(ApiConnector):
    """
    Connector for NCBI Entrez API.

    Provides access to NCBI databases including:
    - PubMed (biomedical literature)
    - GenBank (genetic sequences)
    - dbSNP (genetic variations)
    - And many others

    Example usage:
        connector = NCBIConnector(email="researcher@university.edu")
        results = connector.search_pubmed("CRISPR gene editing", max_results=100)
    """

    def __init__(
        self,
        email: str,
        api_key: Optional[str] = None,
        tool_name: str = "ApiLinker",
        **kwargs,
    ):
        """
        Initialize NCBI connector.

        Args:
            email: Required by NCBI API for identification
            api_key: Optional API key for higher rate limits
            tool_name: Tool name for NCBI logs
            **kwargs: Additional connector arguments
        """
        # NCBI Entrez base URL
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

        # Standard parameters for all NCBI requests
        default_params = {"email": email, "tool": tool_name}

        if api_key:
            default_params["api_key"] = api_key

        # Define common NCBI endpoints
        endpoints = {
            "search": {
                "path": "/esearch.fcgi",
                "method": "GET",
                "params": {**default_params, "retmode": "json"},
            },
            "fetch": {
                "path": "/efetch.fcgi",
                "method": "GET",
                "params": default_params,
            },
            "summary": {
                "path": "/esummary.fcgi",
                "method": "GET",
                "params": {**default_params, "retmode": "json"},
            },
            "link": {
                "path": "/elink.fcgi",
                "method": "GET",
                "params": {**default_params, "retmode": "json"},
            },
        }

        super().__init__(
            connector_type="ncbi",
            base_url=base_url,
            auth_config=None,  # NCBI uses email/API key in parameters
            endpoints=endpoints,
            **kwargs,
        )

        self.email = email
        self.api_key = api_key
        self.tool_name = tool_name

    def search_pubmed(
        self, query: str, max_results: int = 20, sort: str = "relevance"
    ) -> Dict[str, Any]:
        """
        Search PubMed database for articles.

        Args:
            query: Search query (e.g., "machine learning genomics")
            max_results: Maximum number of results to return
            sort: Sort order ("relevance", "date", "first_author", etc.)

        Returns:
            Dictionary containing search results with PubMed IDs
        """
        params = {"db": "pubmed", "term": query, "retmax": max_results, "sort": sort}

        return self.fetch_data("search", params)

    def search_genbank(
        self, query: str, max_results: int = 20, sequence_type: str = "nucleotide"
    ) -> Dict[str, Any]:
        """
        Search GenBank for genetic sequences.

        Args:
            query: Search query (e.g., "Homo sapiens BRCA1")
            max_results: Maximum number of results
            sequence_type: "nucleotide" or "protein"

        Returns:
            Dictionary containing search results with GenBank IDs
        """
        db = "nuccore" if sequence_type == "nucleotide" else "protein"

        params = {"db": db, "term": query, "retmax": max_results}

        return self.fetch_data("search", params)

    def get_article_summaries(self, pubmed_ids: List[str]) -> Dict[str, Any]:
        """
        Get article summaries for PubMed IDs.

        Args:
            pubmed_ids: List of PubMed ID strings

        Returns:
            Dictionary containing article summaries
        """
        params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmax": len(pubmed_ids)}

        return self.fetch_data("summary", params)

    def get_full_articles(self, pubmed_ids: List[str], format: str = "abstract") -> str:
        """
        Get full article data for PubMed IDs.

        Args:
            pubmed_ids: List of PubMed ID strings
            format: "abstract", "medline", "xml", etc.

        Returns:
            Raw article data as string
        """
        params = {
            "db": "pubmed",
            "id": ",".join(pubmed_ids),
            "rettype": format,
            "retmode": "text",
        }

        # Note: This returns raw text, not JSON
        response = self.client.request(
            method="GET",
            url=self.endpoints["fetch"].path,
            params={**self.endpoints["fetch"].params, **params},
        )
        response.raise_for_status()
        return response.text

    def get_sequences(self, genbank_ids: List[str], format: str = "fasta") -> str:
        """
        Get genetic sequences for GenBank IDs.

        Args:
            genbank_ids: List of GenBank ID strings
            format: "fasta", "gb", "xml", etc.

        Returns:
            Raw sequence data as string
        """
        params = {
            "db": "nuccore",
            "id": ",".join(genbank_ids),
            "rettype": format,
            "retmode": "text",
        }

        response = self.client.request(
            method="GET",
            url=self.endpoints["fetch"].path,
            params={**self.endpoints["fetch"].params, **params},
        )
        response.raise_for_status()
        return response.text

    def find_related_articles(
        self, pubmed_ids: List[str], link_type: str = "pubmed_pubmed"
    ) -> Dict[str, Any]:
        """
        Find articles related to given PubMed IDs.

        Args:
            pubmed_ids: List of PubMed ID strings
            link_type: Type of relationship to find

        Returns:
            Dictionary containing related article IDs
        """
        params = {
            "dbfrom": "pubmed",
            "db": "pubmed",
            "id": ",".join(pubmed_ids),
            "linkname": link_type,
        }

        return self.fetch_data("link", params)

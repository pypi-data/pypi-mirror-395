"""
CrossRef API connector for citation data and DOI resolution.

Provides access to CrossRef's REST API for academic citation data,
journal metadata, and bibliographic information.
"""

from typing import Any, Dict, Optional
from apilinker.core.connector import ApiConnector


class CrossRefConnector(ApiConnector):
    """
    Connector for CrossRef API.

    Provides access to citation data, DOI resolution, journal metadata,
    and bibliographic information from CrossRef's database.

    Example usage:
        connector = CrossRefConnector(email="researcher@university.edu")
        papers = connector.search_papers("machine learning", max_results=100)
        citations = connector.get_citations_for_doi("10.1038/nature12373")
    """

    def __init__(self, email: str, **kwargs):
        """
        Initialize CrossRef connector.

        Args:
            email: Contact email (recommended by CrossRef for polite pool)
            **kwargs: Additional connector arguments
        """
        # CrossRef REST API base URL
        base_url = "https://api.crossref.org"

        # Set up headers for polite pool access
        headers = {"User-Agent": f"ApiLinker/0.5.4 (mailto:{email})"}

        # Define CrossRef endpoints
        endpoints = {
            "search_works": {"path": "/works", "method": "GET", "params": {}},
            "get_work": {"path": "/works/{doi}", "method": "GET", "params": {}},
            "search_journals": {"path": "/journals", "method": "GET", "params": {}},
            "get_journal": {"path": "/journals/{issn}", "method": "GET", "params": {}},
            "search_funders": {"path": "/funders", "method": "GET", "params": {}},
        }

        super().__init__(
            connector_type="crossref",
            base_url=base_url,
            auth_config=None,  # CrossRef API is open access
            endpoints=endpoints,
            headers=headers,
            **kwargs,
        )

        self.email = email

    def search_papers(
        self,
        query: str,
        max_results: int = 20,
        sort: str = "relevance",
        filters: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Search for academic papers.

        Args:
            query: Search query
            max_results: Maximum number of results
            sort: Sort order ("relevance", "score", "updated", "deposited", "indexed", "published")
            filters: Additional filters (e.g., {"type": "journal-article", "from-pub-date": "2020"})

        Returns:
            Dictionary containing search results
        """
        params = {"query": query, "rows": max_results, "sort": sort}

        # Add filters if provided
        if filters:
            for key, value in filters.items():
                params[f"filter"] = f"{key}:{value}"

        return self.fetch_data("search_works", params)

    def get_paper_by_doi(self, doi: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific DOI.

        Args:
            doi: Digital Object Identifier

        Returns:
            Dictionary containing paper details
        """
        # Remove any URL prefix from DOI
        clean_doi = doi.replace("https://doi.org/", "").replace(
            "http://dx.doi.org/", ""
        )

        endpoint_path = self.endpoints["get_work"].path.format(doi=clean_doi)

        response = self.client.request(
            method="GET", url=endpoint_path, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def search_by_author(
        self, author_name: str, max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Search for papers by author name.

        Args:
            author_name: Author name to search
            max_results: Maximum number of results

        Returns:
            Dictionary containing search results
        """
        return self.search_papers(
            query=f'author:"{author_name}"', max_results=max_results, sort="published"
        )

    def search_by_journal(
        self, journal_name: str, year: Optional[int] = None, max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Search for papers in a specific journal.

        Args:
            journal_name: Name of the journal
            year: Publication year filter
            max_results: Maximum number of results

        Returns:
            Dictionary containing search results
        """
        filters = {"type": "journal-article"}
        if year:
            filters["from-pub-date"] = str(year)
            filters["until-pub-date"] = str(year)

        return self.search_papers(
            query=f'container-title:"{journal_name}"',
            max_results=max_results,
            filters=filters,
        )

    def get_citation_data(
        self, doi: str, include_references: bool = True
    ) -> Dict[str, Any]:
        """
        Get citation data for a paper.

        Args:
            doi: Digital Object Identifier
            include_references: Whether to include reference list

        Returns:
            Dictionary containing citation information
        """
        paper_data = self.get_paper_by_doi(doi)

        # Extract citation-relevant information
        citation_info = {
            "doi": doi,
            "title": paper_data.get("message", {}).get("title", ["Unknown"])[0],
            "authors": paper_data.get("message", {}).get("author", []),
            "journal": paper_data.get("message", {}).get(
                "container-title", ["Unknown"]
            )[0],
            "published_date": self._extract_date(paper_data.get("message", {})),
            "citation_count": paper_data.get("message", {}).get(
                "is-referenced-by-count", 0
            ),
            "reference_count": paper_data.get("message", {}).get("references-count", 0),
        }

        if include_references and "reference" in paper_data.get("message", {}):
            citation_info["references"] = paper_data["message"]["reference"]

        return citation_info

    def search_recent_papers(
        self, subject_area: str, days_back: int = 30, max_results: int = 100
    ) -> Dict[str, Any]:
        """
        Search for recent papers in a subject area.

        Args:
            subject_area: Subject area to search
            days_back: How many days back to search
            max_results: Maximum number of results

        Returns:
            Dictionary containing recent papers
        """
        from datetime import datetime, timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        filters = {
            "from-pub-date": start_date.strftime("%Y-%m-%d"),
            "until-pub-date": end_date.strftime("%Y-%m-%d"),
        }

        return self.search_papers(
            query=subject_area,
            max_results=max_results,
            sort="published",
            filters=filters,
        )

    def get_journal_metrics(self, issn: str) -> Dict[str, Any]:
        """
        Get metrics for a journal.

        Args:
            issn: ISSN of the journal

        Returns:
            Dictionary containing journal metrics
        """
        endpoint_path = self.endpoints["get_journal"].path.format(issn=issn)

        response = self.client.request(
            method="GET", url=endpoint_path, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def search_funded_research(
        self, funder_name: str, max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Search for research funded by a specific organization.

        Args:
            funder_name: Name of the funding organization
            max_results: Maximum number of results

        Returns:
            Dictionary containing funded research
        """
        return self.search_papers(
            query=f'funder:"{funder_name}"', max_results=max_results, sort="published"
        )

    def _extract_date(self, paper_data: Dict[str, Any]) -> Optional[str]:
        """Extract publication date from paper data."""
        date_parts = paper_data.get(
            "published-print", paper_data.get("published-online", {})
        )

        if "date-parts" in date_parts and date_parts["date-parts"]:
            parts = date_parts["date-parts"][0]
            if len(parts) >= 3:
                return f"{parts[0]}-{parts[1]:02d}-{parts[2]:02d}"
            elif len(parts) >= 2:
                return f"{parts[0]}-{parts[1]:02d}-01"
            elif len(parts) >= 1:
                return f"{parts[0]}-01-01"

        return None

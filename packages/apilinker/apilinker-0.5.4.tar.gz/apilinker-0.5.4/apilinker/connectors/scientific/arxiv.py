"""
arXiv API connector for academic preprint papers.

Provides access to arXiv's API for searching and retrieving
academic papers across various scientific disciplines.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Dict, List, Optional
from apilinker.core.connector import ApiConnector


class ArXivConnector(ApiConnector):
    """
    Connector for arXiv API.

    Provides access to arXiv preprint repository for academic papers
    across physics, mathematics, computer science, and other fields.

    Example usage:
        connector = ArXivConnector()
        results = connector.search_papers("machine learning", max_results=50)
    """

    def __init__(self, **kwargs):
        """Initialize arXiv connector."""

        # arXiv API base URL (tests expect HTTP)
        base_url = "http://export.arxiv.org/api"

        # Define arXiv endpoints
        endpoints = {"query": {"path": "/query", "method": "GET", "params": {}}}

        super().__init__(
            connector_type="arxiv",
            base_url=base_url,
            auth_config=None,  # arXiv API doesn't require authentication
            endpoints=endpoints,
            **kwargs,
        )

    def search_papers(
        self,
        query: str,
        max_results: int = 10,
        start: int = 0,
        sort_by: str = "relevance",
        sort_order: str = "descending",
        category: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search arXiv for papers.

        Args:
            query: Search query (e.g., "machine learning", "quantum computing")
            max_results: Maximum number of results to return
            start: Starting index for pagination
            sort_by: "relevance", "lastUpdatedDate", "submittedDate"
            sort_order: "ascending" or "descending"
            category: Optional category filter (e.g., "cs.AI", "physics:hep-th")

        Returns:
            List of paper dictionaries with metadata
        """
        # Build search query
        search_query = query
        if category:
            search_query = f"cat:{category} AND {query}" if query else f"cat:{category}"

        params = {
            "search_query": search_query,
            "start": start,
            "max_results": max_results,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }

        # Get raw XML response
        response = self.client.request(
            method="GET", url=self.endpoints["query"].path, params=params
        )
        response.raise_for_status()

        # Parse XML response
        return self._parse_arxiv_response(response.text)

    def get_paper_by_id(self, arxiv_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific paper by arXiv ID.

        Args:
            arxiv_id: arXiv identifier (e.g., "2301.00001" or "cs.AI/0001001")

        Returns:
            Paper dictionary or None if not found
        """
        params = {"id_list": arxiv_id, "max_results": 1}

        response = self.client.request(
            method="GET", url=self.endpoints["query"].path, params=params
        )
        response.raise_for_status()

        papers = self._parse_arxiv_response(response.text)
        return papers[0] if papers else None

    def search_by_author(
        self, author_name: str, max_results: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search for papers by author name.

        Args:
            author_name: Author name to search for
            max_results: Maximum number of results

        Returns:
            List of paper dictionaries
        """
        return self.search_papers(
            query=f'au:"{author_name}"',
            max_results=max_results,
            sort_by="submittedDate",
        )

    def search_recent_papers(
        self, category: str, days_back: int = 7, max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get recent papers from a specific category.

        Args:
            category: arXiv category (e.g., "cs.AI", "physics:astro-ph")
            days_back: How many days back to search
            max_results: Maximum number of results

        Returns:
            List of recent paper dictionaries
        """
        return self.search_papers(
            query="",
            category=category,
            max_results=max_results,
            sort_by="submittedDate",
            sort_order="descending",
        )

    def _parse_arxiv_response(self, xml_content: str) -> List[Dict[str, Any]]:
        """
        Parse arXiv XML response into structured data.

        Args:
            xml_content: Raw XML response from arXiv API

        Returns:
            List of parsed paper dictionaries
        """
        papers = []

        try:
            # Parse XML
            root = ET.fromstring(xml_content)

            # Define namespaces
            namespaces = {
                "atom": "http://www.w3.org/2005/Atom",
                "arxiv": "http://arxiv.org/schemas/atom",
            }

            # Extract entries
            entries = root.findall("atom:entry", namespaces)

            for entry in entries:
                paper = {}

                # Basic metadata
                paper["id"] = self._get_text(entry, "atom:id", namespaces)
                paper["title"] = self._get_text(
                    entry, "atom:title", namespaces, ""
                ).strip()
                paper["summary"] = self._get_text(
                    entry, "atom:summary", namespaces, ""
                ).strip()

                # Extract arXiv ID from URL
                arxiv_id = paper["id"].split("/")[-1] if paper.get("id") else ""
                paper["arxiv_id"] = arxiv_id

                # Authors
                authors = []
                author_elements = entry.findall("atom:author", namespaces)
                for author in author_elements:
                    name = self._get_text(author, "atom:name", namespaces)
                    if name:
                        authors.append(name)
                paper["authors"] = authors

                # Categories
                categories = []
                category_elements = entry.findall("atom:category", namespaces)
                for cat in category_elements:
                    term = cat.get("term")
                    if term:
                        categories.append(term)
                paper["categories"] = categories

                # Dates
                published = self._get_text(entry, "atom:published", namespaces)
                updated = self._get_text(entry, "atom:updated", namespaces)

                paper["published_date"] = self._parse_date(published)
                paper["updated_date"] = self._parse_date(updated)

                # Links
                links = {}
                link_elements = entry.findall("atom:link", namespaces)
                for link in link_elements:
                    rel = link.get("rel", "")
                    href = link.get("href", "")
                    title = link.get("title", "")

                    if rel == "alternate":
                        links["abstract_url"] = href
                    elif title == "pdf":
                        links["pdf_url"] = href
                    elif title == "doi":
                        links["doi_url"] = href

                paper["links"] = links

                # arXiv-specific metadata
                comment = self._get_text(entry, "arxiv:comment", namespaces)
                journal_ref = self._get_text(entry, "arxiv:journal_ref", namespaces)
                doi = self._get_text(entry, "arxiv:doi", namespaces)

                if comment:
                    paper["comment"] = comment
                if journal_ref:
                    paper["journal_reference"] = journal_ref
                if doi:
                    paper["doi"] = doi

                papers.append(paper)

        except ET.ParseError as e:
            raise ValueError(f"Failed to parse arXiv XML response: {e}")

        return papers

    def _get_text(
        self,
        element: ET.Element,
        path: str,
        namespaces: Dict[str, str],
        default: str = None,
    ) -> Optional[str]:
        """Helper to safely extract text from XML element."""
        found = element.find(path, namespaces)
        return found.text if found is not None else default

    def _parse_date(self, date_str: Optional[str]) -> Optional[str]:
        """Parse arXiv date string to ISO format."""
        if not date_str:
            return None

        try:
            # arXiv dates are in format: 2023-01-15T09:30:00Z
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.isoformat()
        except (ValueError, AttributeError):
            return date_str  # Return original if parsing fails

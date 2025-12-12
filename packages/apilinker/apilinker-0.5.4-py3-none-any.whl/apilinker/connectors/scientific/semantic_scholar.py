"""
Semantic Scholar API connector for AI-powered academic search.

Provides access to Semantic Scholar's API for academic papers with
AI-enhanced search, citation analysis, and research recommendations.
"""

from typing import Any, Dict, List, Optional
from apilinker.core.connector import ApiConnector


class SemanticScholarConnector(ApiConnector):
    """
    Connector for Semantic Scholar API.

    Provides AI-powered academic search, citation analysis, author profiles,
    and research recommendations using Semantic Scholar's database.

    Example usage:
        connector = SemanticScholarConnector(api_key="your-key")
        papers = connector.search_papers("transformer neural networks")
        author_info = connector.get_author_info("Paul G. Allen")
        recommendations = connector.get_recommendations_for_paper("paper_id")
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Semantic Scholar connector.

        Args:
            api_key: Optional API key for higher rate limits
            **kwargs: Additional connector arguments
        """
        # Semantic Scholar API base URL
        base_url = "https://api.semanticscholar.org/graph/v1"

        # Set up headers
        headers = {"User-Agent": "ApiLinker/0.5.4"}
        if api_key:
            headers["x-api-key"] = api_key

        # Define Semantic Scholar endpoints
        endpoints = {
            "search_papers": {"path": "/paper/search", "method": "GET", "params": {}},
            "get_paper": {"path": "/paper/{paper_id}", "method": "GET", "params": {}},
            "get_paper_citations": {
                "path": "/paper/{paper_id}/citations",
                "method": "GET",
                "params": {},
            },
            "get_paper_references": {
                "path": "/paper/{paper_id}/references",
                "method": "GET",
                "params": {},
            },
            "search_authors": {"path": "/author/search", "method": "GET", "params": {}},
            "get_author": {
                "path": "/author/{author_id}",
                "method": "GET",
                "params": {},
            },
            "get_author_papers": {
                "path": "/author/{author_id}/papers",
                "method": "GET",
                "params": {},
            },
            "get_recommendations": {
                "path": "/recommendations",
                "method": "POST",
                "params": {},
            },
        }

        super().__init__(
            connector_type="semantic_scholar",
            base_url=base_url,
            auth_config=None,  # API key is handled in headers
            endpoints=endpoints,
            headers=headers,
            **kwargs,
        )

        self.api_key = api_key

    def search_papers(
        self,
        query: str,
        max_results: int = 100,
        fields: Optional[List[str]] = None,
        year_filter: Optional[str] = None,
        venue_filter: Optional[str] = None,
        min_citation_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Search for academic papers using AI-powered search.

        Args:
            query: Search query
            max_results: Maximum number of results (max 100 per request)
            fields: Fields to return (title, authors, year, citationCount, etc.)
            year_filter: Year filter (e.g., "2020-2024", "2023")
            venue_filter: Publication venue filter
            min_citation_count: Minimum citation count filter

        Returns:
            Dictionary containing search results with AI-enhanced relevance
        """
        if fields is None:
            fields = [
                "paperId",
                "title",
                "abstract",
                "authors",
                "year",
                "citationCount",
                "referenceCount",
                "influentialCitationCount",
                "venue",
                "publicationDate",
                "publicationTypes",
                "s2FieldsOfStudy",
            ]

        params = {
            "query": query,
            "limit": min(max_results, 100),  # API limit is 100
            "fields": ",".join(fields),
        }

        # Add filters
        if year_filter:
            params["year"] = year_filter
        if venue_filter:
            params["venue"] = venue_filter
        if min_citation_count:
            params["minCitationCount"] = min_citation_count

        return self.fetch_data("search_papers", params)

    def get_paper_details(
        self,
        paper_id: str,
        include_citations: bool = False,
        include_references: bool = False,
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific paper.

        Args:
            paper_id: Semantic Scholar paper ID or DOI
            include_citations: Whether to include citing papers
            include_references: Whether to include referenced papers

        Returns:
            Dictionary containing detailed paper information
        """
        fields = [
            "paperId",
            "title",
            "abstract",
            "authors",
            "year",
            "citationCount",
            "referenceCount",
            "influentialCitationCount",
            "venue",
            "publicationDate",
            "publicationTypes",
            "s2FieldsOfStudy",
            "embedding",  # Semantic embedding for similarity
        ]

        params = {"fields": ",".join(fields)}

        # Get basic paper info
        endpoint_path = self.endpoints["get_paper"].path.format(paper_id=paper_id)

        response = self.client.request(
            method="GET", url=endpoint_path, params=params, headers=self.headers
        )
        response.raise_for_status()
        paper_data = response.json()

        # Add citations if requested
        if include_citations:
            citations = self.get_paper_citations(paper_id, limit=100)
            paper_data["citations"] = citations.get("data", [])

        # Add references if requested
        if include_references:
            references = self.get_paper_references(paper_id, limit=100)
            paper_data["references"] = references.get("data", [])

        return paper_data

    def get_paper_citations(self, paper_id: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get papers that cite a specific paper.

        Args:
            paper_id: Semantic Scholar paper ID or DOI
            limit: Maximum number of citations to return

        Returns:
            Dictionary containing citing papers
        """
        params = {
            "limit": limit,
            "fields": "paperId,title,authors,year,citationCount,venue",
        }

        endpoint_path = self.endpoints["get_paper_citations"].path.format(
            paper_id=paper_id
        )

        response = self.client.request(
            method="GET", url=endpoint_path, params=params, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_paper_references(self, paper_id: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get papers referenced by a specific paper.

        Args:
            paper_id: Semantic Scholar paper ID or DOI
            limit: Maximum number of references to return

        Returns:
            Dictionary containing referenced papers
        """
        params = {
            "limit": limit,
            "fields": "paperId,title,authors,year,citationCount,venue",
        }

        endpoint_path = self.endpoints["get_paper_references"].path.format(
            paper_id=paper_id
        )

        response = self.client.request(
            method="GET", url=endpoint_path, params=params, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def search_authors(self, query: str, limit: int = 50) -> Dict[str, Any]:
        """
        Search for authors.

        Args:
            query: Author name or search query
            limit: Maximum number of results

        Returns:
            Dictionary containing author search results
        """
        params = {
            "query": query,
            "limit": limit,
            "fields": "authorId,name,affiliations,paperCount,citationCount,hIndex",
        }

        return self.fetch_data("search_authors", params)

    def get_author_info(
        self, author_id: str, include_recent_papers: bool = True
    ) -> Dict[str, Any]:
        """
        Get detailed information about an author.

        Args:
            author_id: Semantic Scholar author ID
            include_recent_papers: Whether to include recent papers

        Returns:
            Dictionary containing author information
        """
        params = {
            "fields": "authorId,name,affiliations,paperCount,citationCount,hIndex"
        }

        endpoint_path = self.endpoints["get_author"].path.format(author_id=author_id)

        response = self.client.request(
            method="GET", url=endpoint_path, params=params, headers=self.headers
        )
        response.raise_for_status()
        author_data = response.json()

        if include_recent_papers:
            recent_papers = self.get_author_papers(author_id, limit=20)
            author_data["recent_papers"] = recent_papers.get("data", [])

        return author_data

    def get_author_papers(
        self, author_id: str, limit: int = 100, sort: str = "year"
    ) -> Dict[str, Any]:
        """
        Get papers by a specific author.

        Args:
            author_id: Semantic Scholar author ID
            limit: Maximum number of papers
            sort: Sort order ("year", "citationCount", "influentialCitationCount")

        Returns:
            Dictionary containing author's papers
        """
        params = {
            "limit": limit,
            "sort": sort,
            "fields": "paperId,title,year,citationCount,venue,publicationTypes",
        }

        endpoint_path = self.endpoints["get_author_papers"].path.format(
            author_id=author_id
        )

        response = self.client.request(
            method="GET", url=endpoint_path, params=params, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_recommendations(
        self, paper_ids: List[str], max_recommendations: int = 20
    ) -> Dict[str, Any]:
        """
        Get AI-powered paper recommendations based on seed papers.

        Args:
            paper_ids: List of paper IDs to base recommendations on
            max_recommendations: Maximum number of recommendations

        Returns:
            Dictionary containing recommended papers
        """
        data = {"positivePaperIds": paper_ids, "limit": max_recommendations}

        response = self.client.request(
            method="POST",
            url=self.endpoints["get_recommendations"].path,
            json=data,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def analyze_research_trends(
        self, topic: str, years: List[int], max_papers_per_year: int = 100
    ) -> Dict[str, Any]:
        """
        Analyze research trends for a topic over multiple years.

        Args:
            topic: Research topic to analyze
            years: List of years to analyze
            max_papers_per_year: Maximum papers to analyze per year

        Returns:
            Dictionary containing trend analysis
        """
        trend_data = {}

        for year in years:
            year_papers = self.search_papers(
                query=topic, max_results=max_papers_per_year, year_filter=str(year)
            )

            papers = year_papers.get("data", [])

            # Calculate metrics for this year
            total_papers = len(papers)
            total_citations = sum(paper.get("citationCount", 0) for paper in papers)
            avg_citations = total_citations / total_papers if total_papers > 0 else 0

            # Extract venues
            venues = {}
            for paper in papers:
                venue = paper.get("venue", "Unknown")
                venues[venue] = venues.get(venue, 0) + 1

            top_venues = sorted(venues.items(), key=lambda x: x[1], reverse=True)[:5]

            trend_data[year] = {
                "total_papers": total_papers,
                "total_citations": total_citations,
                "avg_citations_per_paper": round(avg_citations, 2),
                "top_venues": top_venues,
            }

        return {
            "topic": topic,
            "years_analyzed": years,
            "trend_data": trend_data,
            "analysis_summary": self._summarize_trends(trend_data),
        }

    def find_similar_papers(
        self, reference_paper_id: str, max_similar: int = 20
    ) -> Dict[str, Any]:
        """
        Find papers similar to a reference paper using AI embeddings.

        Args:
            reference_paper_id: ID of the reference paper
            max_similar: Maximum number of similar papers

        Returns:
            Dictionary containing similar papers
        """
        # Get recommendations based on single paper
        recommendations = self.get_recommendations([reference_paper_id], max_similar)

        # Also get papers that cite this paper (may be similar)
        citations = self.get_paper_citations(reference_paper_id, limit=max_similar)

        return {
            "reference_paper_id": reference_paper_id,
            "ai_recommendations": recommendations.get("data", []),
            "citing_papers": citations.get("data", []),
        }

    def _summarize_trends(self, trend_data: Dict[int, Dict]) -> Dict[str, Any]:
        """Summarize trend analysis data."""
        years = sorted(trend_data.keys())

        if len(years) < 2:
            return {"summary": "Insufficient data for trend analysis"}

        # Calculate growth rates
        first_year = years[0]
        last_year = years[-1]

        paper_growth = (
            (
                trend_data[last_year]["total_papers"]
                - trend_data[first_year]["total_papers"]
            )
            / trend_data[first_year]["total_papers"]
            * 100
            if trend_data[first_year]["total_papers"] > 0
            else 0
        )

        citation_growth = (
            (
                trend_data[last_year]["total_citations"]
                - trend_data[first_year]["total_citations"]
            )
            / trend_data[first_year]["total_citations"]
            * 100
            if trend_data[first_year]["total_citations"] > 0
            else 0
        )

        return {
            "paper_count_growth_percent": round(paper_growth, 1),
            "citation_count_growth_percent": round(citation_growth, 1),
            "trend_direction": (
                "growing"
                if paper_growth > 10
                else "stable" if paper_growth > -10 else "declining"
            ),
            "research_maturity": (
                "mature"
                if trend_data[last_year]["avg_citations_per_paper"] > 10
                else "emerging"
            ),
        }

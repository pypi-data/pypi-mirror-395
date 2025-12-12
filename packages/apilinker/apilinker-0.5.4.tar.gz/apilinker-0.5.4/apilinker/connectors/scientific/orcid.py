"""
ORCID API connector for researcher identification and profile data.

Provides access to ORCID's API for researcher profiles, publications,
affiliations, and academic credentials.
"""

from typing import Any, Dict, List, Optional
from apilinker.core.connector import ApiConnector


class ORCIDConnector(ApiConnector):
    """
    Connector for ORCID API.

    Provides access to researcher profiles, publications, employment history,
    education, and other academic credentials via ORCID's REST API.

    Example usage:
        connector = ORCIDConnector()
        researcher = connector.search_researchers("John Smith machine learning")
        profile = connector.get_researcher_profile("0000-0000-0000-0000")
        works = connector.get_researcher_works("0000-0000-0000-0000")
    """

    def __init__(self, access_token: Optional[str] = None, **kwargs):
        """
        Initialize ORCID connector.

        Args:
            access_token: Optional OAuth access token for authenticated requests
            **kwargs: Additional connector arguments
        """
        # ORCID API base URL (public API)
        base_url = "https://pub.orcid.org/v3.0"

        # Set up headers
        headers = {"Accept": "application/json", "User-Agent": "ApiLinker/0.5.4"}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        # Define ORCID endpoints
        endpoints = {
            "search": {"path": "/search", "method": "GET", "params": {}},
            "get_record": {"path": "/{orcid_id}/record", "method": "GET", "params": {}},
            "get_person": {"path": "/{orcid_id}/person", "method": "GET", "params": {}},
            "get_works": {"path": "/{orcid_id}/works", "method": "GET", "params": {}},
            "get_work_details": {
                "path": "/{orcid_id}/work/{put_code}",
                "method": "GET",
                "params": {},
            },
            "get_employments": {
                "path": "/{orcid_id}/employments",
                "method": "GET",
                "params": {},
            },
            "get_educations": {
                "path": "/{orcid_id}/educations",
                "method": "GET",
                "params": {},
            },
            "get_fundings": {
                "path": "/{orcid_id}/fundings",
                "method": "GET",
                "params": {},
            },
        }

        super().__init__(
            connector_type="orcid",
            base_url=base_url,
            auth_config=None,  # Auth handled via headers
            endpoints=endpoints,
            headers=headers,
            **kwargs,
        )

        self.access_token = access_token

    def search_researchers(
        self,
        query: str,
        max_results: int = 50,
        search_fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Search for researchers by name, affiliation, or keywords.

        Args:
            query: Search query (name, affiliation, keywords)
            max_results: Maximum number of results
            search_fields: Specific fields to search in

        Returns:
            Dictionary containing researcher search results
        """
        params = {"q": query, "rows": max_results}

        # Add field-specific search if specified
        if search_fields:
            # ORCID supports field-specific searches like:
            # given-names:John AND family-name:Smith
            # affiliation-org-name:"Stanford University"
            formatted_query = self._format_field_search(query, search_fields)
            params["q"] = formatted_query

        return self.fetch_data("search", params)

    def get_researcher_profile(
        self,
        orcid_id: str,
        include_works: bool = True,
        include_employment: bool = True,
        include_education: bool = True,
    ) -> Dict[str, Any]:
        """
        Get comprehensive researcher profile.

        Args:
            orcid_id: ORCID identifier (e.g., "0000-0000-0000-0000")
            include_works: Whether to include publication list
            include_employment: Whether to include employment history
            include_education: Whether to include education history

        Returns:
            Dictionary containing comprehensive researcher profile
        """
        # Clean ORCID ID format
        clean_orcid = self._clean_orcid_id(orcid_id)

        # Get basic record
        record_path = self.endpoints["get_record"].path.format(orcid_id=clean_orcid)

        response = self.client.request(
            method="GET", url=record_path, headers=self.headers
        )
        response.raise_for_status()
        profile = response.json()

        # Add additional sections if requested
        if include_works:
            try:
                works = self.get_researcher_works(clean_orcid)
                profile["works_summary"] = works
            except Exception:
                profile["works_summary"] = {"note": "Works data not available"}

        if include_employment:
            try:
                employment = self.get_employment_history(clean_orcid)
                profile["employment_summary"] = employment
            except Exception:
                profile["employment_summary"] = {
                    "note": "Employment data not available"
                }

        if include_education:
            try:
                education = self.get_education_history(clean_orcid)
                profile["education_summary"] = education
            except Exception:
                profile["education_summary"] = {"note": "Education data not available"}

        return profile

    def get_researcher_works(
        self, orcid_id: str, include_details: bool = False, max_works: int = 100
    ) -> Dict[str, Any]:
        """
        Get researcher's published works.

        Args:
            orcid_id: ORCID identifier
            include_details: Whether to fetch detailed information for each work
            max_works: Maximum number of works to return

        Returns:
            Dictionary containing researcher's works
        """
        clean_orcid = self._clean_orcid_id(orcid_id)

        works_path = self.endpoints["get_works"].path.format(orcid_id=clean_orcid)

        response = self.client.request(
            method="GET", url=works_path, headers=self.headers
        )
        response.raise_for_status()
        works_data = response.json()

        if include_details and "group" in works_data:
            detailed_works = []

            for group in works_data["group"][:max_works]:
                for work_summary in group.get("work-summary", []):
                    put_code = work_summary["put-code"]

                    try:
                        work_details = self.get_work_details(clean_orcid, put_code)
                        detailed_works.append(work_details)
                    except Exception:
                        # If detailed info fails, keep summary
                        detailed_works.append(work_summary)

            works_data["detailed_works"] = detailed_works

        return works_data

    def get_work_details(self, orcid_id: str, put_code: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific work.

        Args:
            orcid_id: ORCID identifier
            put_code: ORCID put-code for the specific work

        Returns:
            Dictionary containing detailed work information
        """
        clean_orcid = self._clean_orcid_id(orcid_id)

        work_path = self.endpoints["get_work_details"].path.format(
            orcid_id=clean_orcid, put_code=put_code
        )

        response = self.client.request(
            method="GET", url=work_path, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_employment_history(self, orcid_id: str) -> Dict[str, Any]:
        """
        Get researcher's employment history.

        Args:
            orcid_id: ORCID identifier

        Returns:
            Dictionary containing employment history
        """
        clean_orcid = self._clean_orcid_id(orcid_id)

        employment_path = self.endpoints["get_employments"].path.format(
            orcid_id=clean_orcid
        )

        response = self.client.request(
            method="GET", url=employment_path, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_education_history(self, orcid_id: str) -> Dict[str, Any]:
        """
        Get researcher's education history.

        Args:
            orcid_id: ORCID identifier

        Returns:
            Dictionary containing education history
        """
        clean_orcid = self._clean_orcid_id(orcid_id)

        education_path = self.endpoints["get_educations"].path.format(
            orcid_id=clean_orcid
        )

        response = self.client.request(
            method="GET", url=education_path, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_funding_history(self, orcid_id: str) -> Dict[str, Any]:
        """
        Get researcher's funding history.

        Args:
            orcid_id: ORCID identifier

        Returns:
            Dictionary containing funding history
        """
        clean_orcid = self._clean_orcid_id(orcid_id)

        funding_path = self.endpoints["get_fundings"].path.format(orcid_id=clean_orcid)

        response = self.client.request(
            method="GET", url=funding_path, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def analyze_researcher_network(
        self, orcid_ids: List[str], include_collaborators: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze collaboration network among researchers.

        Args:
            orcid_ids: List of ORCID identifiers to analyze
            include_collaborators: Whether to include co-author analysis

        Returns:
            Dictionary containing network analysis
        """
        network_data = {
            "researchers": {},
            "collaborations": [],
            "institutions": {},
            "research_areas": {},
        }

        for orcid_id in orcid_ids:
            try:
                # Get researcher profile
                profile = self.get_researcher_profile(
                    orcid_id, include_works=True, include_employment=True
                )

                network_data["researchers"][orcid_id] = {
                    "name": self._extract_name(profile),
                    "current_affiliation": self._extract_current_affiliation(profile),
                    "work_count": self._count_works(profile),
                    "research_areas": self._extract_research_areas(profile),
                }

                # Extract institutional affiliations
                affiliations = self._extract_all_affiliations(profile)
                for affiliation in affiliations:
                    if affiliation not in network_data["institutions"]:
                        network_data["institutions"][affiliation] = []
                    network_data["institutions"][affiliation].append(orcid_id)

            except Exception as e:
                network_data["researchers"][orcid_id] = {
                    "error": f"Failed to retrieve data: {str(e)}"
                }

        # Analyze institutional collaborations
        network_data["institutional_collaborations"] = (
            self._analyze_institutional_collaborations(network_data["institutions"])
        )

        return network_data

    def search_by_affiliation(
        self, institution_name: str, max_results: int = 100
    ) -> Dict[str, Any]:
        """
        Search for researchers by institutional affiliation.

        Args:
            institution_name: Name of the institution
            max_results: Maximum number of results

        Returns:
            Dictionary containing researchers from the institution
        """
        # Format query for affiliation search
        query = f'affiliation-org-name:"{institution_name}"'

        return self.search_researchers(query, max_results)

    def search_by_research_area(
        self, research_keywords: List[str], max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Search for researchers by research area keywords.

        Args:
            research_keywords: List of research keywords
            max_results: Maximum number of results

        Returns:
            Dictionary containing researchers in the research area
        """
        # Combine keywords with OR logic
        query = " OR ".join([f'keyword:"{keyword}"' for keyword in research_keywords])

        return self.search_researchers(query, max_results)

    def _clean_orcid_id(self, orcid_id: str) -> str:
        """Clean and format ORCID ID."""
        # Remove any prefixes and ensure proper format
        clean_id = orcid_id.replace("https://orcid.org/", "").replace(
            "http://orcid.org/", ""
        )

        # Ensure proper format (0000-0000-0000-0000)
        if len(clean_id) == 16 and "-" not in clean_id:
            clean_id = (
                f"{clean_id[:4]}-{clean_id[4:8]}-{clean_id[8:12]}-{clean_id[12:]}"
            )

        return clean_id

    def _format_field_search(self, query: str, search_fields: List[str]) -> str:
        """Format query for field-specific search."""
        # This is a simplified implementation
        # In practice, you'd parse the query and apply field-specific formatting
        if "name" in search_fields:
            parts = query.split()
            if len(parts) >= 2:
                return f"given-names:{parts[0]} AND family-name:{parts[1]}"

        return query

    def _extract_name(self, profile: Dict[str, Any]) -> str:
        """Extract researcher name from profile."""
        try:
            person = profile.get("person", {})
            name = person.get("name", {})

            given_names = name.get("given-names", {}).get("value", "")
            family_name = name.get("family-name", {}).get("value", "")

            return f"{given_names} {family_name}".strip()
        except Exception:
            return "Name not available"

    def _extract_current_affiliation(self, profile: Dict[str, Any]) -> str:
        """Extract current institutional affiliation."""
        try:
            employments = profile.get("employment_summary", {}).get(
                "employment-summary", []
            )

            if employments:
                # Get most recent employment
                latest = employments[0]  # Usually sorted by recency
                org_name = latest.get("organization", {}).get("name", "Unknown")
                return org_name

            return "No current affiliation listed"
        except Exception:
            return "Affiliation not available"

    def _count_works(self, profile: Dict[str, Any]) -> int:
        """Count number of works in profile."""
        try:
            works = profile.get("works_summary", {})
            if "group" in works:
                return len(works["group"])
            return 0
        except Exception:
            return 0

    def _extract_research_areas(self, profile: Dict[str, Any]) -> List[str]:
        """Extract research areas from works and keywords."""
        research_areas = []

        try:
            # Extract from keywords if available
            person = profile.get("person", {})
            keywords = person.get("keywords", {}).get("keyword", [])

            for keyword in keywords:
                if isinstance(keyword, dict) and "content" in keyword:
                    research_areas.append(keyword["content"])
                elif isinstance(keyword, str):
                    research_areas.append(keyword)

        except Exception:
            pass

        return research_areas

    def _extract_all_affiliations(self, profile: Dict[str, Any]) -> List[str]:
        """Extract all institutional affiliations from profile."""
        affiliations = []

        try:
            # From employment
            employments = profile.get("employment_summary", {}).get(
                "employment-summary", []
            )
            for emp in employments:
                org_name = emp.get("organization", {}).get("name")
                if org_name and org_name not in affiliations:
                    affiliations.append(org_name)

            # From education
            educations = profile.get("education_summary", {}).get(
                "education-summary", []
            )
            for edu in educations:
                org_name = edu.get("organization", {}).get("name")
                if org_name and org_name not in affiliations:
                    affiliations.append(org_name)

        except Exception:
            pass

        return affiliations

    def _analyze_institutional_collaborations(
        self, institutions: Dict[str, List[str]]
    ) -> List[Dict]:
        """Analyze collaborations between institutions."""
        collaborations = []

        institution_list = list(institutions.keys())

        for i, inst1 in enumerate(institution_list):
            for inst2 in institution_list[i + 1 :]:
                shared_researchers = len(
                    set(institutions[inst1]) & set(institutions[inst2])
                )

                if shared_researchers > 0:
                    collaborations.append(
                        {
                            "institution_1": inst1,
                            "institution_2": inst2,
                            "shared_researchers": shared_researchers,
                            "collaboration_strength": (
                                "strong"
                                if shared_researchers > 5
                                else "moderate" if shared_researchers > 2 else "weak"
                            ),
                        }
                    )

        return sorted(
            collaborations, key=lambda x: x["shared_researchers"], reverse=True
        )

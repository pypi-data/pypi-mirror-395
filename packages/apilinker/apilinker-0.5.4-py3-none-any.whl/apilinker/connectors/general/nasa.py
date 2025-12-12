"""
NASA Open Data API connector for climate, earth science, and space research.

Provides access to NASA's various APIs for earth observation data,
climate information, and space science research.
"""

from typing import Any, Dict, List, Optional, Union
from apilinker.core.connector import ApiConnector


class NASAConnector(ApiConnector):
    """
    Connector for NASA Open Data APIs.

    Provides access to NASA's earth science data, climate information,
    astronomy data, and other space science resources.

    Example usage:
        connector = NASAConnector(api_key="nasa_api_key")
        earth_data = connector.get_earth_imagery(lat=40.7128, lon=-74.0060)
        climate_data = connector.search_climate_data("temperature", "2023-01-01", "2023-12-31")
        apod = connector.get_astronomy_picture_of_day()
    """

    def __init__(self, api_key: Optional[str] = "DEMO_KEY", **kwargs):
        """
        Initialize NASA connector.

        Args:
            api_key: NASA API key (get from https://api.nasa.gov/).
                    Defaults to "DEMO_KEY" for testing (limited rate).
            **kwargs: Additional connector arguments
        """
        # NASA API base URL
        base_url = "https://api.nasa.gov"

        # Define NASA endpoints
        endpoints = {
            "earth_imagery": {
                "path": "/planetary/earth/imagery",
                "method": "GET",
                "params": {"api_key": api_key},
            },
            "earth_assets": {
                "path": "/planetary/earth/assets",
                "method": "GET",
                "params": {"api_key": api_key},
            },
            "apod": {
                "path": "/planetary/apod",
                "method": "GET",
                "params": {"api_key": api_key},
            },
            "neo_feed": {
                "path": "/neo/rest/v1/feed",
                "method": "GET",
                "params": {"api_key": api_key},
            },
            "mars_weather": {
                "path": "/insight_weather/",
                "method": "GET",
                "params": {"api_key": api_key, "feedtype": "json", "ver": "1.0"},
            },
            "exoplanet_archive": {
                "path": "/exoplanet/rest/ps",
                "method": "GET",
                "params": {},
            },
            "techport": {
                "path": "/techport/api/projects",
                "method": "GET",
                "params": {},
            },
        }

        super().__init__(
            connector_type="nasa",
            base_url=base_url,
            auth_config=None,  # API key passed in params
            endpoints=endpoints,
            **kwargs,
        )

        self.api_key = api_key

    def get_earth_imagery(
        self, lat: float, lon: float, date: Optional[str] = None, dim: float = 0.1
    ) -> Dict[str, Any]:
        """
        Get Landsat 8 earth imagery for a location.

        Args:
            lat: Latitude
            lon: Longitude
            date: Date in YYYY-MM-DD format (defaults to most recent)
            dim: Width/height of image in degrees

        Returns:
            Dictionary containing imagery information
        """
        params = {"lat": lat, "lon": lon, "dim": dim, "api_key": self.api_key}

        if date:
            params["date"] = date

        return self.fetch_data("earth_imagery", params)

    def get_earth_assets(
        self, lat: float, lon: float, date: Optional[str] = None, dim: float = 0.1
    ) -> Dict[str, Any]:
        """
        Get available earth imagery assets for a location.

        Args:
            lat: Latitude
            lon: Longitude
            date: Date in YYYY-MM-DD format
            dim: Width/height in degrees

        Returns:
            Dictionary containing available assets
        """
        params = {"lat": lat, "lon": lon, "dim": dim, "api_key": self.api_key}

        if date:
            params["date"] = date

        return self.fetch_data("earth_assets", params)

    def get_astronomy_picture_of_day(
        self,
        date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        count: Optional[int] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Get Astronomy Picture of the Day.

        Args:
            date: Specific date (YYYY-MM-DD)
            start_date: Start date for range (YYYY-MM-DD)
            end_date: End date for range (YYYY-MM-DD)
            count: Number of random images to retrieve

        Returns:
            Dictionary or list of dictionaries with APOD data
        """
        params = {"api_key": self.api_key}

        if date:
            params["date"] = date
        elif start_date and end_date:
            params["start_date"] = start_date
            params["end_date"] = end_date
        elif count:
            params["count"] = count

        return self.fetch_data("apod", params)

    def get_near_earth_objects(
        self, start_date: str, end_date: str, detailed: bool = False
    ) -> Dict[str, Any]:
        """
        Get Near Earth Objects data.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD, max 7 days from start)
            detailed: Whether to include detailed orbital data

        Returns:
            Dictionary containing NEO data
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "detailed": str(detailed).lower(),
            "api_key": self.api_key,
        }

        return self.fetch_data("neo_feed", params)

    def search_climate_data(
        self,
        parameter: str,
        start_date: str,
        end_date: str,
        location: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Search climate and earth science data.

        Note: This is a conceptual method. Actual implementation would
        require access to specific NASA climate data APIs.

        Args:
            parameter: Climate parameter (temperature, precipitation, etc.)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            location: Optional location dict with lat/lon

        Returns:
            Dictionary containing climate data search results
        """
        # This would connect to NASA's Earth Data APIs
        # For now, returning a structured placeholder
        return {
            "parameter": parameter,
            "date_range": {"start": start_date, "end": end_date},
            "location": location,
            "note": "Climate data search requires specific NASA Earth Data API integration",
            "suggested_apis": [
                "Giovanni (GES DISC)",
                "Goddard Earth Sciences Data and Information Services Center",
                "NASA Earthdata Search",
            ],
        }

    def get_mars_weather(self) -> Dict[str, Any]:
        """
        Get Mars weather data from InSight mission.

        Note: InSight mission ended, but this shows the pattern
        for accessing planetary weather data.

        Returns:
            Dictionary containing Mars weather data
        """
        try:
            return self.fetch_data("mars_weather", {})
        except Exception:
            return {
                "note": "Mars InSight weather data no longer available",
                "status": "mission_ended",
                "alternative": "Consider Mars 2020 Perseverance weather data",
            }

    def search_exoplanets(
        self,
        planet_name: Optional[str] = None,
        discovery_method: Optional[str] = None,
        discovery_year: Optional[int] = None,
        max_results: int = 100,
    ) -> Dict[str, Any]:
        """
        Search NASA Exoplanet Archive.

        Args:
            planet_name: Specific planet name
            discovery_method: Discovery method filter
            discovery_year: Discovery year filter
            max_results: Maximum number of results

        Returns:
            Dictionary containing exoplanet data
        """
        # NASA Exoplanet Archive uses different base URL

        base_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

        # Build ADQL query
        query_parts = ["SELECT TOP {} * FROM ps".format(max_results)]

        where_conditions = []
        if planet_name:
            where_conditions.append(f"pl_name LIKE '%{planet_name}%'")
        if discovery_method:
            where_conditions.append(f"discoverymethod = '{discovery_method}'")
        if discovery_year:
            where_conditions.append(f"disc_year = {discovery_year}")

        if where_conditions:
            query_parts.append("WHERE " + " AND ".join(where_conditions))

        query = " ".join(query_parts)

        params = {"query": query, "format": "json"}

        # Direct request to exoplanet archive
        response = self.client.request(method="GET", url=base_url, params=params)
        response.raise_for_status()

        return {"query": query, "results": response.json() if response.content else []}

    def get_nasa_techport_projects(
        self,
        search_term: Optional[str] = None,
        mission_directorate: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search NASA TechPort for technology projects.

        Args:
            search_term: Search term for projects
            mission_directorate: NASA mission directorate filter

        Returns:
            Dictionary containing NASA technology projects
        """
        params = {}

        if search_term:
            params["searchTerm"] = search_term
        if mission_directorate:
            params["missionDirectorate"] = mission_directorate

        try:
            return self.fetch_data("techport", params)
        except Exception:
            return {
                "note": "TechPort API access may require special permissions",
                "search_term": search_term,
                "mission_directorate": mission_directorate,
            }

    def analyze_earth_observation_trends(
        self,
        locations: List[Dict[str, float]],
        date_range: Dict[str, str],
        parameters: List[str],
    ) -> Dict[str, Any]:
        """
        Analyze earth observation trends across multiple locations.

        Args:
            locations: List of location dicts with lat/lon
            date_range: Dict with start_date and end_date
            parameters: List of parameters to analyze

        Returns:
            Dictionary containing trend analysis
        """
        analysis = {
            "locations": locations,
            "date_range": date_range,
            "parameters": parameters,
            "location_analysis": {},
            "temporal_trends": {},
        }

        # For each location, get available earth imagery/data
        for i, location in enumerate(locations):
            location_key = f"location_{i+1}"

            try:
                # Get earth assets for this location
                assets = self.get_earth_assets(
                    lat=location["lat"],
                    lon=location["lon"],
                    date=date_range.get("end_date"),
                )

                analysis["location_analysis"][location_key] = {
                    "coordinates": location,
                    "available_assets": assets,
                    "data_availability": "available" if assets else "limited",
                }

            except Exception as e:
                analysis["location_analysis"][location_key] = {
                    "coordinates": location,
                    "error": str(e),
                    "data_availability": "unavailable",
                }

        return analysis

    def get_space_weather_data(
        self, start_date: str, end_date: str, data_type: str = "solar_flare"
    ) -> Dict[str, Any]:
        """
        Get space weather data.

        Note: This is a conceptual method. Actual implementation would
        require access to NOAA Space Weather APIs or NASA space weather data.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            data_type: Type of space weather data

        Returns:
            Dictionary containing space weather information
        """
        return {
            "data_type": data_type,
            "date_range": {"start": start_date, "end": end_date},
            "note": "Space weather data requires integration with NOAA SWPC or other space weather APIs",
            "suggested_sources": [
                "NOAA Space Weather Prediction Center",
                "NASA Space Weather Research",
                "ESA Space Weather Service Network",
            ],
        }

    def research_climate_indicators(
        self, indicators: List[str], regions: List[str], time_period: str = "annual"
    ) -> Dict[str, Any]:
        """
        Research climate change indicators.

        Args:
            indicators: List of climate indicators (temperature, precipitation, etc.)
            regions: List of geographic regions
            time_period: Time period for analysis

        Returns:
            Dictionary containing climate research data
        """
        research_framework = {
            "indicators": indicators,
            "regions": regions,
            "time_period": time_period,
            "data_sources": {
                "satellite_observations": "NASA Earth observing satellites",
                "climate_models": "NASA GISS climate models",
                "ground_measurements": "NASA surface measurement networks",
            },
            "analysis_framework": {
                "trend_analysis": "Long-term climate trend identification",
                "anomaly_detection": "Climate anomaly identification",
                "correlation_analysis": "Cross-indicator correlations",
                "spatial_analysis": "Geographic pattern analysis",
            },
            "note": "Full implementation requires access to NASA GISS, MODIS, and other climate data APIs",
        }

        return research_framework

    def get_satellite_data(
        self,
        satellite: str,
        instrument: str,
        start_date: str,
        end_date: str,
        location: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Get satellite instrument data.

        Args:
            satellite: Satellite name (e.g., "MODIS", "Landsat")
            instrument: Instrument name
            start_date: Start date
            end_date: End date
            location: Optional location filter

        Returns:
            Dictionary containing satellite data information
        """
        return {
            "satellite": satellite,
            "instrument": instrument,
            "date_range": {"start": start_date, "end": end_date},
            "location": location,
            "note": "Satellite data access requires integration with NASA Earthdata APIs",
            "access_methods": [
                "NASA Earthdata Search",
                "Giovanni (GES DISC)",
                "AppEEARS (LP DAAC)",
                "Direct API access via NASA APIs",
            ],
        }

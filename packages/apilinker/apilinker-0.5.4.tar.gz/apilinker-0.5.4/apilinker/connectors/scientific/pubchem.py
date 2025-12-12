"""
PubChem API connector for chemical compound and bioactivity data.

Provides access to PubChem's REST API for chemical compounds,
bioassays, and substance data - essential for drug discovery research.
"""

from typing import Any, Dict, List, Optional, Union
from apilinker.core.connector import ApiConnector


class PubChemConnector(ApiConnector):
    """
    Connector for PubChem API.

    Provides access to chemical compound data, bioassays, and substance
    information from PubChem's database - crucial for drug discovery,
    chemical biology, and pharmaceutical research.

    Example usage:
        connector = PubChemConnector()
        aspirin = connector.search_compounds("aspirin")
        compound_info = connector.get_compound_by_cid(2244)  # Aspirin CID
        bioassays = connector.search_bioassays("kinase inhibitor")
    """

    def __init__(self, **kwargs):
        """
        Initialize PubChem connector.

        Args:
            **kwargs: Additional connector arguments
        """
        # PubChem REST API base URL
        base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

        # Define PubChem endpoints
        endpoints = {
            "search_compounds": {
                "path": "/compound/name/{name}/JSON",
                "method": "GET",
                "params": {},
            },
            "get_compound_by_cid": {
                "path": "/compound/cid/{cid}/JSON",
                "method": "GET",
                "params": {},
            },
            "search_by_smiles": {
                "path": "/compound/smiles/{smiles}/JSON",
                "method": "GET",
                "params": {},
            },
            "search_bioassays": {
                "path": "/assay/name/{name}/JSON",
                "method": "GET",
                "params": {},
            },
            "get_compound_properties": {
                "path": "/compound/cid/{cid}/property/{properties}/JSON",
                "method": "GET",
                "params": {},
            },
            "similarity_search": {
                "path": "/compound/similarity/smiles/{smiles}/JSON",
                "method": "GET",
                "params": {},
            },
            "substructure_search": {
                "path": "/compound/substructure/smiles/{smiles}/JSON",
                "method": "GET",
                "params": {},
            },
        }

        super().__init__(
            connector_type="pubchem",
            base_url=base_url,
            auth_config=None,  # PubChem API is public
            endpoints=endpoints,
            **kwargs,
        )

    def search_compounds(
        self, compound_name: str, max_results: int = 100
    ) -> Dict[str, Any]:
        """
        Search for chemical compounds by name.

        Args:
            compound_name: Name of the compound to search
            max_results: Maximum number of results

        Returns:
            Dictionary containing compound search results
        """
        # Clean compound name for URL
        clean_name = compound_name.replace(" ", "%20")

        endpoint_path = self.endpoints["search_compounds"].path.format(name=clean_name)

        response = self.client.request(method="GET", url=endpoint_path)
        response.raise_for_status()
        return response.json()

    def get_compound_by_cid(
        self, cid: Union[str, int], include_properties: bool = True
    ) -> Dict[str, Any]:
        """
        Get detailed compound information by CID (Compound ID).

        Args:
            cid: PubChem Compound ID
            include_properties: Whether to include computed properties

        Returns:
            Dictionary containing detailed compound information
        """
        endpoint_path = self.endpoints["get_compound_by_cid"].path.format(cid=str(cid))

        response = self.client.request(
            method="GET", url=endpoint_path, headers=self.headers
        )
        response.raise_for_status()
        compound_data = response.json()

        if include_properties:
            properties = self.get_compound_properties(cid)
            compound_data["computed_properties"] = properties

        return compound_data

    def get_compound_properties(
        self, cid: Union[str, int], properties: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get computed properties for a compound.

        Args:
            cid: PubChem Compound ID
            properties: List of properties to retrieve (if None, gets common ones)

        Returns:
            Dictionary containing compound properties
        """
        if properties is None:
            # Common drug-like properties
            properties = [
                "MolecularWeight",
                "XLogP",
                "HydrogenBondDonorCount",
                "HydrogenBondAcceptorCount",
                "RotatableBondCount",
                "TopologicalPolarSurfaceArea",
                "Complexity",
            ]

        property_string = ",".join(properties)
        endpoint_path = self.endpoints["get_compound_properties"].path.format(
            cid=str(cid), properties=property_string
        )

        response = self.client.request(
            method="GET", url=endpoint_path, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def search_by_smiles(
        self, smiles: str, search_type: str = "exact"
    ) -> Dict[str, Any]:
        """
        Search for compounds by SMILES string.

        Args:
            smiles: SMILES notation of the compound
            search_type: "exact", "similarity", or "substructure"

        Returns:
            Dictionary containing search results
        """
        import urllib.parse

        # URL encode SMILES string
        encoded_smiles = urllib.parse.quote(smiles, safe="")

        if search_type == "exact":
            endpoint_path = self.endpoints["search_by_smiles"].path.format(
                smiles=encoded_smiles
            )
        elif search_type == "similarity":
            endpoint_path = self.endpoints["similarity_search"].path.format(
                smiles=encoded_smiles
            )
        elif search_type == "substructure":
            endpoint_path = self.endpoints["substructure_search"].path.format(
                smiles=encoded_smiles
            )
        else:
            raise ValueError(
                "search_type must be 'exact', 'similarity', or 'substructure'"
            )

        response = self.client.request(
            method="GET", url=endpoint_path, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def search_bioassays(
        self, assay_name: str, max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Search for bioassays by name or description.

        Args:
            assay_name: Name or description of the bioassay
            max_results: Maximum number of results

        Returns:
            Dictionary containing bioassay search results
        """
        clean_name = assay_name.replace(" ", "%20")
        endpoint_path = self.endpoints["search_bioassays"].path.format(name=clean_name)

        response = self.client.request(
            method="GET", url=endpoint_path, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_drug_like_compounds(
        self, target_name: str, apply_lipinski_filter: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search for drug-like compounds targeting a specific protein/pathway.

        Args:
            target_name: Name of the target (e.g., "kinase", "GPCR")
            apply_lipinski_filter: Whether to apply Lipinski's Rule of Five

        Returns:
            List of drug-like compounds with their properties
        """
        # Search for compounds related to the target
        compounds = self.search_compounds(target_name)

        drug_like_compounds = []

        if "PC_Compounds" in compounds:
            for compound in compounds["PC_Compounds"][:20]:  # Limit to first 20
                cid = compound["id"]["id"]["cid"]

                # Get properties
                try:
                    properties = self.get_compound_properties(cid)

                    if apply_lipinski_filter:
                        # Apply Lipinski's Rule of Five
                        if self._passes_lipinski_filter(properties):
                            compound_data = {
                                "cid": cid,
                                "properties": properties,
                                "lipinski_compliant": True,
                            }
                            drug_like_compounds.append(compound_data)
                    else:
                        compound_data = {
                            "cid": cid,
                            "properties": properties,
                            "lipinski_compliant": self._passes_lipinski_filter(
                                properties
                            ),
                        }
                        drug_like_compounds.append(compound_data)

                except Exception:
                    continue  # Skip if properties can't be retrieved

        return drug_like_compounds

    def analyze_compound_similarity(
        self,
        reference_smiles: str,
        similarity_threshold: float = 0.8,
        max_results: int = 100,
    ) -> Dict[str, Any]:
        """
        Find compounds similar to a reference compound.

        Args:
            reference_smiles: SMILES string of reference compound
            similarity_threshold: Tanimoto similarity threshold (0.0-1.0)
            max_results: Maximum number of similar compounds

        Returns:
            Dictionary containing similar compounds and analysis
        """
        similar_compounds = self.search_by_smiles(
            reference_smiles, search_type="similarity"
        )

        analysis = {
            "reference_smiles": reference_smiles,
            "similarity_threshold": similarity_threshold,
            "similar_compounds": [],
            "structural_diversity": None,
        }

        if "PC_Compounds" in similar_compounds:
            compounds = similar_compounds["PC_Compounds"][:max_results]

            for compound in compounds:
                cid = compound["id"]["id"]["cid"]

                # Get basic info and properties
                try:
                    compound_info = self.get_compound_by_cid(
                        cid, include_properties=True
                    )
                    analysis["similar_compounds"].append(
                        {"cid": cid, "compound_info": compound_info}
                    )
                except Exception:
                    continue

            # Calculate structural diversity (simplified)
            analysis["structural_diversity"] = self._calculate_diversity_metrics(
                analysis["similar_compounds"]
            )

        return analysis

    def search_drug_targets(
        self, drug_name: str, include_pathways: bool = True
    ) -> Dict[str, Any]:
        """
        Search for biological targets of a drug compound.

        Args:
            drug_name: Name of the drug
            include_pathways: Whether to include pathway information

        Returns:
            Dictionary containing target and pathway information
        """
        # First, find the compound
        compound_results = self.search_compounds(drug_name)

        target_info = {
            "drug_name": drug_name,
            "compound_cid": None,
            "bioassays": [],
            "targets": [],
            "pathways": [] if include_pathways else None,
        }

        if "PC_Compounds" in compound_results and compound_results["PC_Compounds"]:
            cid = compound_results["PC_Compounds"][0]["id"]["id"]["cid"]
            target_info["compound_cid"] = cid

            # Search for bioassays involving this compound
            try:
                # This would require additional PubChem API calls
                # For now, provide structure for future implementation
                target_info["note"] = (
                    "Target identification requires additional bioassay analysis"
                )
            except Exception:
                pass

        return target_info

    def _search_compounds_by_synonym(
        self, compound_name: str, max_results: int
    ) -> Dict[str, Any]:
        """Search compounds using synonym/alternative name approach."""
        # Alternative search method using different endpoint
        # This is a simplified implementation
        return {"note": "Synonym search not yet implemented", "query": compound_name}

    def _passes_lipinski_filter(self, properties: Dict[str, Any]) -> bool:
        """Check if compound passes Lipinski's Rule of Five."""
        try:
            props = properties.get("PropertyTable", {}).get("Properties", [])
            if not props:
                return False

            prop_dict = {}
            for prop in props:
                if "MolecularWeight" in prop:
                    prop_dict["molecular_weight"] = prop["MolecularWeight"]
                if "XLogP" in prop:
                    prop_dict["logp"] = prop["XLogP"]
                if "HydrogenBondDonorCount" in prop:
                    prop_dict["hbd"] = prop["HydrogenBondDonorCount"]
                if "HydrogenBondAcceptorCount" in prop:
                    prop_dict["hba"] = prop["HydrogenBondAcceptorCount"]

            # Lipinski's Rule of Five
            lipinski_violations = 0

            if prop_dict.get("molecular_weight", 0) > 500:
                lipinski_violations += 1
            if prop_dict.get("logp", 0) > 5:
                lipinski_violations += 1
            if prop_dict.get("hbd", 0) > 5:
                lipinski_violations += 1
            if prop_dict.get("hba", 0) > 10:
                lipinski_violations += 1

            return lipinski_violations <= 1  # Allow 1 violation

        except Exception:
            return False

    def _calculate_diversity_metrics(self, compounds: List[Dict]) -> Dict[str, Any]:
        """Calculate simple diversity metrics for a set of compounds."""
        if not compounds:
            return {"diversity_score": 0, "note": "No compounds to analyze"}

        # Simplified diversity calculation based on property ranges
        molecular_weights = []
        logp_values = []

        for compound in compounds:
            try:
                props = compound.get("compound_info", {}).get("computed_properties", {})
                props_list = props.get("PropertyTable", {}).get("Properties", [])

                for prop in props_list:
                    if "MolecularWeight" in prop:
                        molecular_weights.append(prop["MolecularWeight"])
                    if "XLogP" in prop:
                        logp_values.append(prop["XLogP"])
            except Exception:
                continue

        diversity_metrics = {
            "compound_count": len(compounds),
            "molecular_weight_range": {
                "min": min(molecular_weights) if molecular_weights else 0,
                "max": max(molecular_weights) if molecular_weights else 0,
                "std": (
                    self._calculate_std(molecular_weights) if molecular_weights else 0
                ),
            },
            "logp_range": {
                "min": min(logp_values) if logp_values else 0,
                "max": max(logp_values) if logp_values else 0,
                "std": self._calculate_std(logp_values) if logp_values else 0,
            },
        }

        return diversity_metrics

    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance**0.5

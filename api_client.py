"""
Devici API Client

Handles authentication and API requests to the Devici platform.
"""

import os
import logging
from typing import Dict, Any, Optional, List, Union
import httpx
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class DeviciConfig(BaseModel):
    """Configuration for Devici API client."""
    api_base_url: str
    client_id: str
    client_secret: str
    debug: bool = False


class DeviciAPIClient:
    """Client for interacting with the Devici API."""
    
    def __init__(self, config: DeviciConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.api_base_url,
            timeout=30.0
        )
        self.access_token: Optional[str] = None
        self.token_type: str = "Bearer"
        
    async def __aenter__(self):
        await self.authenticate()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()
        
    async def authenticate(self) -> None:
        """Authenticate with Devici API and get access token."""
        auth_data = {
            "clientId": self.config.client_id,
            "secret": self.config.client_secret
        }
        
        try:
            response = await self.client.post("/auth", json=auth_data)
            response.raise_for_status()
            auth_response = response.json()
            
            self.access_token = auth_response["access_token"]
            self.token_type = auth_response.get("token_type", "Bearer")
            
            # Set authorization header for future requests
            self.client.headers["Authorization"] = f"{self.token_type} {self.access_token}"
            
            logger.info("Successfully authenticated with Devici API")
            
        except httpx.HTTPError as e:
            logger.error(f"Authentication failed: {e}")
            raise
            
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make authenticated request to Devici API."""
        if not self.access_token:
            await self.authenticate()
            
        try:
            response = await self.client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json_data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"API request failed: {method} {endpoint} - {e}")
            raise
            
    # User Management
    async def get_users(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get all users."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/users/", params=params)
        
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get specific user by ID."""
        return await self._make_request("GET", f"/users/{user_id}")
        
    async def search_users(self, field: str, text: str) -> Dict[str, Any]:
        """Search users by field and text."""
        return await self._make_request("GET", f"/users/search/field={field}&text={text}")
        
    async def bulk_invite_users(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk invite users."""
        return await self._make_request("POST", "/users/bulk-invite", json_data={"payload": users})
        
    async def invite_user(self, email: str, first_name: str, last_name: str, role: str) -> Dict[str, Any]:
        """Invite specific user."""
        user_data = {
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "role": role
        }
        return await self._make_request("POST", "/users/invite", json_data=user_data)
        
    async def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update specific user."""
        return await self._make_request("PUT", f"/users/{user_id}", json_data=user_data)
        
    async def delete_user(self, user_id: str) -> None:
        """Delete specific user."""
        await self._make_request("DELETE", f"/users/{user_id}")
        
    # Collections Management
    async def get_collections(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get all collections."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/collections/", params=params)
        
    async def get_collection(self, collection_id: str) -> Dict[str, Any]:
        """Get specific collection by ID."""
        return await self._make_request("GET", f"/collections/{collection_id}")
        
    async def create_collection(self, collection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new collection."""
        return await self._make_request("POST", "/collections", json_data=collection_data)
        
    async def update_collection(self, collection_id: str, collection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update specific collection."""
        return await self._make_request("PUT", f"/collections/{collection_id}", json_data=collection_data)
        
    async def delete_collection(self, collection_id: str) -> None:
        """Delete specific collection."""
        await self._make_request("DELETE", f"/collections/{collection_id}")
        
    # Threat Models Management
    async def get_threat_models(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get all threat models."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/threat-models/", params=params)
        
    async def get_threat_models_by_collection(self, collection_id: str, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get all threat models by collection."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", f"/threat-models/collection/{collection_id}", params=params)
        
    async def get_threat_model(self, threat_model_id: str) -> Dict[str, Any]:
        """Get specific threat model by ID."""
        return await self._make_request("GET", f"/threat-models/{threat_model_id}")
        
    async def create_threat_model(self, threat_model_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new threat model."""
        return await self._make_request("POST", "/threat-models", json_data=threat_model_data)
        
    async def update_threat_model(self, threat_model_id: str, threat_model_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update specific threat model."""
        return await self._make_request("PUT", f"/threat-models/{threat_model_id}", json_data=threat_model_data)
        
    async def delete_threat_model(self, threat_model_id: str) -> None:
        """Delete specific threat model."""
        await self._make_request("DELETE", f"/threat-models/{threat_model_id}")
        
    async def import_otm_file(self, collection_id: str, otm_file_path: str) -> Dict[str, Any]:
        """Import an OTM file by creating a complete threat model with components, threats, and mitigations."""
        import json
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Read OTM file content
        with open(otm_file_path, 'r') as f:
            otm_content = json.load(f)
        
        # Extract project information from OTM
        project = otm_content.get("project", {})
        title = project.get("name", "Imported Threat Model")
        description = project.get("description", "Threat model imported from OTM file")
        
        logger.info(f"Starting OTM import for: {title}")
        
        # Step 1: Create the threat model
        threat_model_data = {
            "title": title,
            "description": description,
            "collectionId": collection_id
        }
        
        threat_model = await self._make_request("POST", "/threat-models", json_data=threat_model_data)
        threat_model_id = threat_model.get("id")
        
        if not threat_model_id:
            raise Exception("Failed to create threat model - no ID returned")
        
        logger.info(f"Created threat model: {threat_model_id}")
        
        # Get the canvas ID for the threat model
        canvases = threat_model.get("canvases", [])
        if not canvases:
            # If no canvas, try to get threat model details to find canvas
            tm_details = await self.get_threat_model(threat_model_id)
            canvases = tm_details.get("canvases", [])
        
        canvas_id = canvases[0] if canvases else None
        if not canvas_id:
            logger.warning("No canvas found for threat model, components may not be properly linked")
        
        # Track created entities for linking
        component_mapping = {}  # OTM ID -> Devici component ID
        threat_mapping = {}     # OTM ID -> Devici threat ID
        mitigation_mapping = {} # OTM ID -> Devici mitigation ID
        
        import_summary = {
            "threat_model": threat_model,
            "components_created": 0,
            "threats_created": 0,
            "mitigations_created": 0,
            "errors": []
        }
        
        # Step 2: Create components
        components = otm_content.get("components", [])
        logger.info(f"Creating {len(components)} components")
        
        for component in components:
            try:
                component_data = {
                    "title": component.get("name", "Untitled Component"),
                    "description": component.get("description", ""),
                    "type": component.get("type", "generic"),
                }
                
                # Add canvas if available
                if canvas_id:
                    component_data["canvasId"] = canvas_id
                
                # Add tags if available
                tags = component.get("tags", [])
                if tags:
                    component_data["tags"] = ", ".join(tags)
                
                created_component = await self.create_component(component_data)
                # API returns {"component": "id", "representation": "canvas_id"} format
                component_id = created_component.get("component") or created_component.get("id")
                
                if component_id:
                    component_mapping[component.get("id")] = component_id
                    import_summary["components_created"] += 1
                    logger.info(f"Created component: {component.get('name')} -> {component_id}")
                    
                    # Add visual node to canvas for component visibility
                    if canvas_id:
                        try:
                            await self._add_component_to_canvas(component_id, canvas_id, import_summary["components_created"])
                            logger.info(f"Added visual node for component: {component.get('name')}")
                        except Exception as canvas_error:
                            logger.warning(f"Failed to add visual node for {component.get('name')}: {canvas_error}")
                
            except Exception as e:
                error_msg = f"Failed to create component {component.get('name', 'Unknown')}: {str(e)}"
                logger.error(error_msg)
                import_summary["errors"].append(error_msg)
        
        # Step 3: Import threats and mitigations using the OTM endpoint
        threats = otm_content.get("threats", [])
        mitigations = otm_content.get("mitigations", [])
        
        if threats or mitigations:
            logger.info(f"Importing {len(threats)} threats and {len(mitigations)} mitigations via CORRECT /threat-models/otm/{collection_id} endpoint")
            
            try:
                # Prepare OTM data for the CORRECT /threat-models/otm/{collection_id} endpoint
                # Update component IDs in threats to reference created components
                updated_threats = []
                for threat in threats:
                    updated_threat = threat.copy()
                    
                    # Update target references to use created component IDs
                    targets = threat.get("targets", [])
                    if targets:
                        updated_targets = []
                        for target in targets:
                            if target in component_mapping:
                                updated_targets.append(component_mapping[target])
                            else:
                                updated_targets.append(target)
                        updated_threat["targets"] = updated_targets
                    
                    updated_threats.append(updated_threat)
                
                # Create OTM data payload for the threats endpoint
                otm_payload = {
                    "otmVersion": otm_content.get("otmVersion", "0.2.0"),
                    "project": project,
                    "threats": updated_threats,
                    "mitigations": mitigations,
                    "threatModelId": threat_model_id  # Link to our created threat model
                }
                
                # Call the OTM import endpoint using the ONLY CORRECT ENDPOINT
                otm_result = await self._make_request("POST", f"/threat-models/otm/{collection_id}", json_data=otm_payload)
                
                # Extract counts from the OTM import result
                if isinstance(otm_result, dict):
                    import_summary["threats_created"] = otm_result.get("threatsCreated", len(threats))
                    import_summary["mitigations_created"] = otm_result.get("mitigationsCreated", len(mitigations))
                    
                    # Add any errors from OTM import
                    otm_errors = otm_result.get("errors", [])
                    import_summary["errors"].extend(otm_errors)
                    
                    logger.info(f"OTM import completed via CORRECT /threat-models/otm/{collection_id} endpoint: {import_summary['threats_created']} threats, {import_summary['mitigations_created']} mitigations")
                else:
                    # Fallback - assume success if we get a non-dict response
                    import_summary["threats_created"] = len(threats)
                    import_summary["mitigations_created"] = len(mitigations)
                    logger.info(f"OTM import completed (response format: {type(otm_result)})")
                
            except Exception as e:
                error_msg = f"Failed to import threats/mitigations via OTM endpoint: {str(e)}"
                logger.error(error_msg)
                import_summary["errors"].append(error_msg)
                
                # Fallback to individual creation if OTM endpoint fails
                logger.info("Falling back to individual threat/mitigation creation")
                
                # Individual threat creation fallback
                for threat in threats:
                    try:
                        threat_data = {
                            "title": threat.get("name", "Untitled Threat"),
                            "description": threat.get("description", ""),
                            "priority": threat.get("severity", "medium").lower(),
                            "status": "open",
                            "source": f"OTM Import: {threat.get('type', threat.get('category', 'Unknown'))}",
                            "is_custom": True
                        }
                        
                        # Find target component
                        targets = threat.get("targets", [])
                        if targets and len(targets) > 0:
                            target_component_otm_id = targets[0]
                            if target_component_otm_id in component_mapping:
                                threat_data["component"] = {"id": component_mapping[target_component_otm_id]}
                        
                        created_threat = await self.create_threat(threat_data)
                        threat_id = created_threat.get("threat") or created_threat.get("id")
                        
                        if threat_id:
                            threat_mapping[threat.get("id")] = threat_id
                            import_summary["threats_created"] += 1
                            logger.info(f"Created threat (fallback): {threat.get('name')} -> {threat_id}")
                        
                    except Exception as fallback_e:
                        error_msg = f"Fallback creation failed for threat {threat.get('name', 'Unknown')}: {str(fallback_e)}"
                        logger.error(error_msg)
                        import_summary["errors"].append(error_msg)
                
                # Individual mitigation creation fallback
                for mitigation in mitigations:
                    try:
                        mitigation_data = {
                            "title": mitigation.get("name", "Untitled Mitigation"),
                            "definition": mitigation.get("description", ""),
                            "is_custom": True
                        }
                        
                        # Try to link to threats
                        reduces_risk = mitigation.get("reducesRisk", [])
                        if reduces_risk and len(reduces_risk) > 0:
                            threat_ref = reduces_risk[0].get("threat")
                            if threat_ref in threat_mapping:
                                mitigation_data["threat"] = {"id": threat_mapping[threat_ref]}
                        
                        created_mitigation = await self.create_mitigation(mitigation_data)
                        mitigation_id = created_mitigation.get("mitigation") or created_mitigation.get("id")
                        
                        if mitigation_id:
                            mitigation_mapping[mitigation.get("id")] = mitigation_id
                            import_summary["mitigations_created"] += 1
                            logger.info(f"Created mitigation (fallback): {mitigation.get('name')} -> {mitigation_id}")
                        
                    except Exception as fallback_e:
                        error_msg = f"Fallback creation failed for mitigation {mitigation.get('name', 'Unknown')}: {str(fallback_e)}"
                        logger.error(error_msg)
                        import_summary["errors"].append(error_msg)
        
        logger.info(f"OTM import completed. Components: {import_summary['components_created']}, Threats: {import_summary['threats_created']}, Mitigations: {import_summary['mitigations_created']}")
        
        return import_summary
        
    async def export_threat_model_pdf(self, threat_model_id: str) -> bytes:
        """Export threat model as PDF report."""
        response = await self.client.get(f"/threat-models/{threat_model_id}/export/pdf")
        response.raise_for_status()
        return response.content
        
    async def export_threat_model_otm(self, threat_model_id: str) -> Dict[str, Any]:
        """Export threat model as OTM file."""
        return await self._make_request("GET", f"/threat-models/{threat_model_id}/export/otm")
        
    # Canvas Management
    async def get_canvases(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get all canvases."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/canvases/", params=params)
        
    async def get_canvas(self, canvas_id: str) -> Dict[str, Any]:
        """Get specific canvas by ID."""
        return await self._make_request("GET", f"/canvases/{canvas_id}")
        
    async def create_canvas(self, canvas_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new canvas."""
        return await self._make_request("POST", "/canvases", json_data=canvas_data)
    
    async def _add_component_to_canvas(self, component_id: str, canvas_id: str, position_index: int) -> None:
        """Add a visual node to canvas for a component to make it visible in the UI."""
        import uuid
        
        # Get current canvas data
        canvas = await self.get_canvas(canvas_id)
        canvas_data = canvas.get('data', {})
        nodes = canvas_data.get('nodes', [])
        edges = canvas_data.get('edges', [])
        
        # Calculate position (spread components in a grid)
        grid_size = 300
        x_pos = (position_index % 3) * grid_size + 200  # 3 columns, start at 200
        y_pos = (position_index // 3) * grid_size + 100  # New row every 3 components
        
        # Get user data for the node (required based on working example)
        # Try to get user info from existing nodes or use a default
        user_data = None
        if nodes:
            user_data = nodes[0].get('data', {}).get('user')
        
        if not user_data:
            # Use minimal user data if none available
            user_data = {
                "id": "8d1f7d98-dca2-4d13-8187-24904cd00366",  # From working example
                "role": "admin",
                "email": "geoff@securitycompass.com",
                "first_name": "Geoff",
                "last_name": "Whittington"
            }
        
        # Create visual node matching the working format
        node_data = {
            "id": str(uuid.uuid4()),
            "data": {
                "id": "",  # Empty string like in working example
                "user": user_data,
                "label": "Process",
                "selectedBy": [],
                "representation": canvas_id
            },
            "type": "processNode",
            "width": 200,
            "height": 150,
            "zIndex": position_index + 1,
            "dragging": False,
            "measured": {
                "width": 200,
                "height": 150
            },
            "position": {
                "x": x_pos,
                "y": y_pos
            },
            "resizing": False,
            "selected": False
        }
        
        # Add node to canvas
        nodes.append(node_data)
        
        # Update canvas with new node - try PATCH instead of PUT
        updated_canvas_data = {
            "data": {
                "nodes": nodes,
                "edges": edges,
                "edgeFloating": canvas_data.get("edgeFloating", {"default": True, "editable": False, "smoothstep": True, "editableBezier": False})
            }
        }
        
        try:
            # Try PATCH first
            await self._make_request("PATCH", f"/canvases/{canvas_id}", json_data=updated_canvas_data)
        except:
            # Fallback to PUT if PATCH fails
            await self._make_request("PUT", f"/canvases/{canvas_id}", json_data=updated_canvas_data)
        
    # Comments Management
    async def get_comments_by_threat(self, threat_id: str) -> Dict[str, Any]:
        """Get all comments for specific threat."""
        return await self._make_request("GET", f"/comments/threat/{threat_id}")
        
    async def create_comment(self, comment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new comment."""
        return await self._make_request("POST", "/comments", json_data=comment_data)
        
    # Codex Management - Knowledge Base
    async def get_codex_threats(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get standardized threats from knowledge base."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/codex/threats/", params=params)
        
    async def search_codex_threats(self, query: str) -> Dict[str, Any]:
        """Search threats in knowledge base."""
        return await self._make_request("GET", f"/codex/threats/search", params={"q": query})
        
    async def get_codex_mitigations(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get standardized mitigations from knowledge base."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/codex/mitigations/", params=params)
        
    async def search_codex_mitigations(self, query: str) -> Dict[str, Any]:
        """Search mitigations in knowledge base."""
        return await self._make_request("GET", f"/codex/mitigations/search", params={"q": query})
        
    # Components Management
    async def get_components(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get all components."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/components/", params=params)
        
    async def get_component(self, component_id: str) -> Dict[str, Any]:
        """Get specific component by ID."""
        return await self._make_request("GET", f"/components/{component_id}")
        
    async def get_components_by_canvas(self, canvas_id: str) -> Dict[str, Any]:
        """Get all components for specific canvas."""
        return await self._make_request("GET", f"/components/canvas/{canvas_id}")
        
    async def create_component(self, component_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new component."""
        return await self._make_request("POST", "/components", json_data=component_data)
        
    async def update_component(self, component_id: str, component_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update specific component."""
        return await self._make_request("PUT", f"/components/{component_id}", json_data=component_data)
        
    async def delete_component(self, component_id: str) -> None:
        """Delete specific component."""
        await self._make_request("DELETE", f"/components/{component_id}")
        
    # Threats Management  
    async def get_threats(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get all threats."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/threats/", params=params)
        
    async def get_threat(self, threat_id: str) -> Dict[str, Any]:
        """Get specific threat by ID."""
        return await self._make_request("GET", f"/threats/{threat_id}")
        
    async def get_threats_by_component(self, component_id: str) -> Dict[str, Any]:
        """Get all threats for specific component."""
        return await self._make_request("GET", f"/threats/component/{component_id}")
        
    async def create_threat(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new threat."""
        return await self._make_request("POST", "/threats", json_data=threat_data)
        
    async def update_threat(self, threat_id: str, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update specific threat."""
        return await self._make_request("PUT", f"/threats/{threat_id}", json_data=threat_data)
        
    async def delete_threat(self, threat_id: str) -> None:
        """Delete specific threat."""
        await self._make_request("DELETE", f"/threats/{threat_id}")
        
    # Mitigations Management
    async def get_mitigations(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get all mitigations."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/mitigations/", params=params)
        
    async def get_mitigation(self, mitigation_id: str) -> Dict[str, Any]:
        """Get specific mitigation by ID."""
        return await self._make_request("GET", f"/mitigations/{mitigation_id}")
        
    async def get_mitigations_by_threat(self, threat_id: str) -> Dict[str, Any]:
        """Get all mitigations for specific threat."""
        return await self._make_request("GET", f"/mitigations/threat/{threat_id}")
        
    async def create_mitigation(self, mitigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new mitigation."""
        return await self._make_request("POST", "/mitigations", json_data=mitigation_data)
        
    async def update_mitigation(self, mitigation_id: str, mitigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update specific mitigation."""
        return await self._make_request("PUT", f"/mitigations/{mitigation_id}", json_data=mitigation_data)
        
    async def delete_mitigation(self, mitigation_id: str) -> None:
        """Delete specific mitigation."""
        await self._make_request("DELETE", f"/mitigations/{mitigation_id}")
        
    # Teams Management
    async def get_teams(self, limit: int = 20, page: int = 0) -> Dict[str, Any]:
        """Get all teams."""
        params = {"limit": limit, "page": page}
        return await self._make_request("GET", "/teams/", params=params)
        
    async def get_team(self, team_id: str) -> Dict[str, Any]:
        """Get specific team by ID."""
        return await self._make_request("GET", f"/teams/{team_id}")
        
    async def create_team(self, teams_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create new teams."""
        return await self._make_request("POST", "/teams", json_data={"payload": teams_data})
        
    async def update_teams(self, teams_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update multiple teams."""
        return await self._make_request("PUT", "/teams", json_data={"payload": teams_data})
        
    async def delete_team(self, team_id: str) -> None:
        """Delete specific team."""
        await self._make_request("DELETE", f"/teams/{team_id}")
        
    # Dashboard & Reports
    async def get_dashboard_types(self) -> Dict[str, Any]:
        """Get dashboard chart types."""
        return await self._make_request("GET", "/dashboard/types")
        
    async def get_dashboard_data(
        self, 
        chart_type: str, 
        limit: int = 20, 
        page: int = 0,
        start: Optional[str] = None,
        end: Optional[str] = None,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get dashboard data by specific chart type."""
        params = {
            "limit": limit,
            "page": page,
            "type": chart_type
        }
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if project_id:
            params["projectId"] = project_id
            
        return await self._make_request("GET", "/dashboard/", params=params)
        
    async def get_threat_models_report(
        self, 
        start: Optional[str] = None, 
        end: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get threat models reports."""
        params = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        return await self._make_request("GET", "/reports/threat-models", params=params)


def create_client_from_env() -> DeviciAPIClient:
    """Create API client from environment variables."""
    config = DeviciConfig(
        api_base_url=os.getenv("DEVICI_API_BASE_URL", "https://api.devici.com/api/v1"),
        client_id=os.getenv("DEVICI_CLIENT_ID", ""),
        client_secret=os.getenv("DEVICI_CLIENT_SECRET", ""),
        debug=os.getenv("DEBUG", "false").lower() == "true"
    )
    
    if not config.client_id or not config.client_secret:
        raise ValueError("DEVICI_CLIENT_ID and DEVICI_CLIENT_SECRET must be set")
        
    return DeviciAPIClient(config) 
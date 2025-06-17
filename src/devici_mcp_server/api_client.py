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
        
    async def bulk_invite_users(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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
        
    async def create_team(self, teams_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create new teams."""
        return await self._make_request("POST", "/teams", json_data={"payload": teams_data})
        
    async def update_teams(self, teams_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Update multiple teams."""
        return await self._make_request("PUT", "/teams", json_data={"payload": teams_data})
        
    async def delete_team(self, team_id: str) -> None:
        """Delete specific team."""
        await self._make_request("DELETE", f"/teams/{team_id}")
        
    # Dashboard & Reports
    async def get_dashboard_types(self) -> List[str]:
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
    ) -> List[Dict[str, Any]]:
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
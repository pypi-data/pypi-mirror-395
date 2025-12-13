"""
API client for communicating with Paved Platform.
"""
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List
from .config import config


class PlatformAPIError(Exception):
    """Exception raised for API errors."""
    pass


class PlatformAPIClient:
    """Client for Paved Platform API."""

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        raw = (base_url or config.platform_url or "").rstrip('/')
        # Normalize: strip trailing '/v1' if provided by user
        if raw.endswith('/v1'):
            raw = raw[:-3]
        elif raw.endswith('/v1/'):
            raw = raw[:-4]
        self.base_url = raw or "https://app.hipaved.com"
        self._api_key = api_key
        self.session = requests.Session()

    @property
    def api_key(self):
        return self._api_key or config.api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        headers = self._headers()
        try:
            response = self.session.request(method=method, url=url, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_detail = response.json().get('detail', str(e))
            except Exception:
                error_detail = response.text or str(e)
            raise PlatformAPIError(f"API Error: {error_detail}") from e
        except requests.exceptions.RequestException as e:
            raise PlatformAPIError(f"Connection error: {str(e)}") from e

    # --- Auth ---
    def login(self, email: str, password: str) -> Dict[str, Any]:
        response = self._request('POST', '/v1/auth/login', json={'email': email, 'password': password})
        return response.json()

    def register(self, email: str, password: str, name: str) -> Dict[str, Any]:
        response = self._request('POST', '/v1/auth/register', json={'email': email, 'password': password, 'name': name})
        return response.json()

    def get_current_user(self) -> Dict[str, Any]:
        response = self._request('GET', '/v1/auth/me')
        return response.json()

    def create_api_key(self, name: str, expires_in_days: Optional[int] = None) -> Dict[str, Any]:
        payload = {'name': name}
        if expires_in_days:
            payload['expires_in_days'] = expires_in_days
        response = self._request('POST', '/v1/auth/api-keys', json=payload)
        return response.json()

    # --- Agents ---
    def list_agents(self, page: int = 1, per_page: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        params = {'page': page, 'per_page': per_page}
        if status:
            params['status'] = status
        response = self._request('GET', '/v1/agents', params=params)
        return response.json()

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        response = self._request('GET', f'/v1/agents/{agent_id}')
        return response.json()

    def upload_agent(
        self,
        name: str,
        agent_tar_path: Path,
        description: Optional[str] = None,
        policies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        config_data = {
            'name': name,
            'description': description or '',
            'config': {
                'runtime': 'python3.11',
                'policies': policies or [],
                'env': {},
                'memory_mb': 512,
                'timeout_seconds': 300,
                'policy_bundle': 'default',
            },
        }
        files = {'agent_tar': ('agent.tar.gz', open(agent_tar_path, 'rb'), 'application/gzip')}
        data = {'config': json.dumps(config_data)}
        url = f"{self.base_url}/v1/agents"
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        try:
            response = self.session.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = response.json().get('detail', str(e))
            except Exception:
                error_detail = response.text or str(e)
            raise PlatformAPIError(f"Upload failed: {error_detail}") from e
        finally:
            for f in files.values():
                if hasattr(f[1], 'close'):
                    f[1].close()

    # --- Invocations ---
    def invoke_agent(self, agent_id: str, payload: Dict[str, Any], async_execution: bool = True, timeout_seconds: Optional[int] = None) -> Dict[str, Any]:
        data = {'payload': payload, 'async': async_execution}
        if timeout_seconds:
            data['timeout_seconds'] = timeout_seconds
        response = self._request('POST', f'/v1/agents/{agent_id}/invoke', json=data)
        return response.json()

    def get_invocation(self, invocation_id: str) -> Dict[str, Any]:
        response = self._request('GET', f'/v1/invocations/{invocation_id}')
        return response.json()

    def get_invocation_logs(self, invocation_id: str) -> Dict[str, Any]:
        response = self._request('GET', f'/v1/invocations/{invocation_id}/logs')
        return response.json()

    def list_invocations(self, agent_id: Optional[str] = None, page: int = 1, per_page: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        params = {'page': page, 'per_page': per_page}
        if agent_id:
            params['agent_id'] = agent_id
        if status:
            params['status'] = status
        response = self._request('GET', '/v1/invocations', params=params)
        return response.json()

    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        response = self._request('DELETE', f'/v1/agents/{agent_id}')
        return response.json()


# Global API client instance
api_client = PlatformAPIClient()

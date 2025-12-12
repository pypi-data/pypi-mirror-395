import requests
from typing import Any, Dict, Optional, TypeVar, Generic
from .types import ApiConfig

T = TypeVar('T')


class ApiClient:
    """Client HTTP pour communiquer avec l'API Ariary"""

    def __init__(self, config: ApiConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })

    def _get_headers(self, requires_secret: bool = True) -> Dict[str, str]:
        """Crée les en-têtes pour la requête"""
        headers = {
            "x-project-id": self.config.projectId,
        }

        if requires_secret:
            headers["x-secret-id"] = self.config.secretId

        return headers

    def post(self, endpoint: str, data: Dict[str, Any], requires_secret: bool = True) -> Any:
        """Effectue une requête POST"""
        headers = self._get_headers(requires_secret)
        url = f"{self.config.baseUrl}{endpoint}"

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)

    def get(self, endpoint: str, requires_secret: bool = True) -> Any:
        """Effectue une requête GET"""
        headers = self._get_headers(requires_secret)
        url = f"{self.config.baseUrl}{endpoint}"

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)

    def patch(self, endpoint: str, data: Dict[str, Any], requires_secret: bool = True) -> Any:
        """Effectue une requête PATCH"""
        headers = self._get_headers(requires_secret)
        url = f"{self.config.baseUrl}{endpoint}"

        try:
            response = self.session.patch(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)

    def put(self, endpoint: str, data: Dict[str, Any], requires_secret: bool = True) -> Any:
        """Effectue une requête PUT"""
        headers = self._get_headers(requires_secret)
        url = f"{self.config.baseUrl}{endpoint}"

        try:
            response = self.session.put(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.exceptions.RequestException):
        """Gère les erreurs API"""
        if hasattr(error, 'response') and error.response is not None:
            status = error.response.status_code
            message = error.response.json().get('message', error.response.reason)
            raise Exception(f"[{status}] {message}")
        raise error

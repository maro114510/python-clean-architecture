from google.cloud import firestore
from typing import Dict, Any, Optional
from .base import DatabaseConnection


class FirestoreConnection(DatabaseConnection):
    def __init__(self, project_id: str, credentials_path: Optional[str] = None):
        self.project_id = project_id
        self.credentials_path = credentials_path
        self._client = None

    async def connect(self):
        if self.credentials_path:
            self._client = firestore.Client.from_service_account_json(
                self.credentials_path, project=self.project_id
            )
        else:
            self._client = firestore.Client(project=self.project_id)
        return self._client

    async def disconnect(self):
        self._client = None

    def get_connection_info(self) -> Dict[str, Any]:
        return {
            "type": "firestore",
            "project_id": self.project_id,
            "credentials_path": self.credentials_path,
        }

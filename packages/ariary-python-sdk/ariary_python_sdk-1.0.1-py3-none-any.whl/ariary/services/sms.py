from typing import List, Optional, Dict, Any
from ..api_client import ApiClient
from ..types import (
    SendSmsDto,
    BulkSmsDto,
    SendSmsResponseDto,
    ResponseSmsDto,
    MultiSmsResponseDto,
    BulkSmsResponseDto,
)


class SmsService:
    """Service pour gérer les SMS"""

    def __init__(self, client: ApiClient):
        self.client = client

    def send_multi_sms(self, sms_data: SendSmsDto) -> MultiSmsResponseDto:
        """Envoie un SMS à plusieurs destinataires avec le même message"""
        data = {
            "phones": sms_data.phones,
            "message": sms_data.message,
        }
        response = self.client.post("/api/sms/multi", data, requires_secret=True)
        return MultiSmsResponseDto(**response)

    def send_bulk_sms(self, bulk_data: BulkSmsDto) -> BulkSmsResponseDto:
        """Envoie des messages différents à différents groupes de destinataires"""
        data = {"messages": bulk_data.messages}
        response = self.client.post("/api/sms/bulk", data, requires_secret=True)
        return BulkSmsResponseDto(**response)

    def get_sms_history(self) -> List[ResponseSmsDto]:
        """Récupère l'historique de tous les SMS envoyés"""
        response = self.client.get("/api/sms", requires_secret=True)
        return [ResponseSmsDto(**item) for item in response]

    def get_sms_by_id(self, sms_id: str) -> ResponseSmsDto:
        """Récupère un SMS spécifique par son ID"""
        response = self.client.get(f"/api/sms/{sms_id}", requires_secret=True)
        return ResponseSmsDto(**response)

    def update_sms(self, sms_id: str, update_data: Dict[str, Any]) -> ResponseSmsDto:
        """Met à jour un SMS par son ID"""
        response = self.client.patch(f"/api/sms/{sms_id}", update_data, requires_secret=True)
        return ResponseSmsDto(**response)

    def delete_sms(self, sms_id: str) -> ResponseSmsDto:
        """Supprime un SMS par son ID"""
        response = self.client.patch(f"/api/sms/{sms_id}", {}, requires_secret=True)
        return ResponseSmsDto(**response)

from typing import List, Optional
from ..api_client import ApiClient
from ..types import CreatePaymentDto, PaymentResponseDto


class PaymentService:
    """Service pour gérer les paiements"""

    def __init__(self, client: ApiClient):
        self.client = client

    def create_payment(self, payment_data: CreatePaymentDto) -> PaymentResponseDto:
        """Crée un nouveau paiement"""
        data = {
            "code": payment_data.code,
            "amount": payment_data.amount,
            "projectId": payment_data.projectId,
        }
        response = self.client.post("/api/payments", data, requires_secret=False)
        return PaymentResponseDto(**response)

    def get_all_payments(self) -> List[PaymentResponseDto]:
        """Récupère tous les paiements"""
        response = self.client.get("/api/payments", requires_secret=False)
        return [PaymentResponseDto(**item) for item in response]

    def get_payment_by_id(self, payment_id: str) -> PaymentResponseDto:
        """Récupère un paiement par son ID"""
        response = self.client.get(f"/api/payments/{payment_id}", requires_secret=False)
        return PaymentResponseDto(**response)

    def update_payment_rest(self, payment_id: str, ticket_code: str) -> PaymentResponseDto:
        """Met à jour le reste d'un paiement"""
        data = {"ticketCode": ticket_code}
        response = self.client.put(f"/api/payments/{payment_id}/rest", data, requires_secret=False)
        return PaymentResponseDto(**response)

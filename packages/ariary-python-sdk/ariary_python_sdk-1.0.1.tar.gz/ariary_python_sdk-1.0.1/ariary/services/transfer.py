from typing import List
from ..api_client import ApiClient
from ..types import SendTransactionDto, SendTransactionResponse


class TransferService:
    """Service pour gérer les transferts d'argent"""

    def __init__(self, client: ApiClient):
        self.client = client

    def send_transaction(self, transaction_data: SendTransactionDto) -> SendTransactionResponse:
        """Envoie une transaction à un numéro de téléphone"""
        data = {
            "phone": transaction_data.phone,
            "amount": transaction_data.amount,
        }
        response = self.client.post("/api/send-transaction", data, requires_secret=True)
        return SendTransactionResponse(**response)

    def get_all_transactions(self) -> List[SendTransactionResponse]:
        """Récupère toutes les transactions de l'application"""
        response = self.client.get("/api/send-transaction", requires_secret=True)
        return [SendTransactionResponse(**item) for item in response]

    def get_transaction_by_id(self, transaction_id: str) -> SendTransactionResponse:
        """Récupère une transaction spécifique par son ID"""
        response = self.client.get(f"/api/send-transaction/{transaction_id}", requires_secret=True)
        return SendTransactionResponse(**response)

    def update_transaction(self, transaction_id: str, transaction_data: SendTransactionDto) -> SendTransactionResponse:
        """Met à jour une transaction (numéro et montant avant traitement)"""
        data = {
            "phone": transaction_data.phone,
            "amount": transaction_data.amount,
        }
        response = self.client.patch(f"/api/send-transaction/{transaction_id}", data, requires_secret=True)
        return SendTransactionResponse(**response)

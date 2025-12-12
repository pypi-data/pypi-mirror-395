from .api_client import ApiClient
from .services import PaymentService, SmsService, TransferService
from .types import ApiConfig


class AriarySDK:
    """SDK client principal pour l'API de paiement Ariary"""

    def __init__(self, config: ApiConfig):
        self.api_client = ApiClient(config)
        self.payment = PaymentService(self.api_client)
        self.sms = SmsService(self.api_client)
        self.transfer = TransferService(self.api_client)

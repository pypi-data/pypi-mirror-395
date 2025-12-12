from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class CreatePaymentDto:
    """Données pour créer un paiement"""
    code: str
    amount: float
    projectId: str


@dataclass
class PaymentResponseDto:
    """Réponse de création/récupération d'un paiement"""
    id: str
    transactionId: str
    amount: float
    rest: float
    projectId: str
    status: str
    parts: List[Dict[str, Any]]
    createdAt: str
    updatedAt: str


@dataclass
class SendSmsDto:
    """Données pour envoyer un SMS à plusieurs numéros"""
    phones: List[str]
    message: str


@dataclass
class BulkSmsDto:
    """Données pour envoyer des SMS différents en masse"""
    messages: List[Dict[str, Any]]


@dataclass
class SendSmsResponseDto:
    """Réponse d'envoi d'un SMS"""
    id: str
    message: str
    phone: str
    status: str
    createdAt: str


@dataclass
class ResponseSmsDto:
    """Réponse de récupération d'un SMS"""
    id: str
    message: str
    phone: str
    status: str
    createdAt: str
    updatedAt: str


@dataclass
class MultiSmsResponseDto:
    """Réponse d'envoi de SMS multiples"""
    status: str
    data: List[Dict[str, Any]]


@dataclass
class BulkSmsResponseDto:
    """Réponse d'envoi de SMS en masse"""
    status: str
    data: List[Dict[str, Any]]


@dataclass
class SendTransactionDto:
    """Données pour envoyer une transaction"""
    phone: str
    amount: float


@dataclass
class SendTransactionResponse:
    """Réponse d'envoi d'une transaction"""
    id: str
    phone: str
    amount: float
    status: str
    message: str
    requestId: str
    projectId: str
    secretId: str
    createdAt: str


@dataclass
class TransactionResponseDto:
    """Réponse de récupération d'une transaction"""
    id: str
    phone: str
    amount: float
    rest: Optional[float] = None
    status: Optional[str] = None
    ticketCode: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


@dataclass
class ApiConfig:
    """Configuration de l'API"""
    apiKey: str
    secretId: str
    projectId: str
    baseUrl: str = "https://fs-pay-rifont.atydago.com/payment"

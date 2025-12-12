# ariary-sdk

SDK officiel Python pour l'API de paiement Ariary. Permet d'envoyer des paiements, des SMS et des transferts d'argent.

## Installation

```bash
pip install ariary-sdk
```

## Configuration

```python
from ariary import AriarySDK, ApiConfig

config = ApiConfig(
    apiKey="votre_api_key",
    secretId="votre_secret_id",
    projectId="votre_project_id"
)

sdk = AriarySDK(config)
```

## Utilisation

### Paiement

```python
from ariary import CreatePaymentDto

# Créer un paiement
payment = sdk.payment.create_payment(CreatePaymentDto(
    code="PAY-K1X2Y3Z4-ABC123",
    amount=5000,
    projectId="votre_project_id"
))

print(payment)

# Récupérer tous les paiements
all_payments = sdk.payment.get_all_payments()

# Récupérer un paiement par ID
payment = sdk.payment.get_payment_by_id(payment.id)

# Mettre à jour le reste d'un paiement
updated = sdk.payment.update_payment_rest(payment.id, "TICKET123")
```

### SMS

```python
from ariary import SendSmsDto, BulkSmsDto

# Envoyer un SMS à plusieurs numéros
result = sdk.sms.send_multi_sms(SendSmsDto(
    phones=["261345678901", "261345678902"],
    message="Bonjour!"
))

# Envoyer des messages différents en masse
bulk_result = sdk.sms.send_bulk_sms(BulkSmsDto(
    messages=[
        {"phones": ["261345678901"], "message": "Message 1"},
        {"phones": ["261345678902"], "message": "Message 2"}
    ]
))

# Récupérer l'historique des SMS
history = sdk.sms.get_sms_history()

# Récupérer un SMS par ID
sms = sdk.sms.get_sms_by_id(sms_id)

# Mettre à jour un SMS
updated = sdk.sms.update_sms(sms_id, {"message": "Nouveau message"})

# Supprimer un SMS
sdk.sms.delete_sms(sms_id)
```

### Transfer

```python
from ariary import SendTransactionDto

# Envoyer une transaction
transaction = sdk.transfer.send_transaction(SendTransactionDto(
    phone="261345678901",
    amount=5000
))

# Récupérer toutes les transactions
all_transactions = sdk.transfer.get_all_transactions()

# Récupérer une transaction par ID
transaction = sdk.transfer.get_transaction_by_id(transaction_id)

# Mettre à jour une transaction
updated = sdk.transfer.update_transaction(transaction_id, SendTransactionDto(
    phone="261345678902",
    amount=10000
))
```

## Types

Tous les types de données sont disponibles dans le module `ariary`:

```python
from ariary import (
    CreatePaymentDto,
    PaymentResponseDto,
    SendSmsDto,
    BulkSmsDto,
    SendSmsResponseDto,
    MultiSmsResponseDto,
    BulkSmsResponseDto,
    ResponseSmsDto,
    SendTransactionDto,
    SendTransactionResponse,
    TransactionResponseDto,
    ApiConfig,
)
```

## License

ISC

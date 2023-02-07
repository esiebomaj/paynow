from django.db import models
from payments.choices import PaymentStatus
from wallets.choices import WalletEntryTypes
import uuid

class Payment(models.Model):
    external_authorization_url = models.CharField(max_length=100, null=True)
    external_access_code = models.CharField(max_length=100, null=True)
    external_reference = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=PaymentStatus.choices, default=PaymentStatus.CREATED)
    purpose = models.CharField(max_length=100, choices=WalletEntryTypes.choices)
    amount = models.IntegerField()
    user_id = models.CharField(max_length=100)
    meta = models.JSONField(default=dict)
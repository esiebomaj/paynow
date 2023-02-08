from django.db import models
from accounts.models import User
from wallets.choices import WalletEntryTypes
from payments.choices import PaymentStatus

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.BigIntegerField(default=0)

    def __str__(self): 
        return "Wallet for {}".format(self.user)

class WalletEntry(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    entry_type = models.CharField(choices=WalletEntryTypes.choices, max_length=100)
    reference = models.CharField(max_length=100) # coresponding payment id 
    description = models.TextField()


class WalletTransfer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="debit_transfers")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="credit_transfers")
    amount = models.IntegerField()
    status = models.CharField(max_length=100, choices=PaymentStatus.choices, default=PaymentStatus.CREATED)
    meta = models.JSONField(default=dict)

from django.utils.translation import gettext as _
from django.db import models

class WalletEntryTypes(models.TextChoices):
    WITHDRAWAL = "withdrawal"
    REVERSE_WITHDRAWAL = "reverse_withdrawal"
    TOPUP = "topup"
    TRANSFER_CREDIT = "transfer_credit"
    TRANSFER_DEBIT = "transfer_debit"
    
    @staticmethod
    def nagated_entries():
        return [WalletEntryTypes.WITHDRAWAL, WalletEntryTypes.TRANSFER_DEBIT]

from django.contrib import admin
from wallets.models import Wallet, WalletEntry, WalletTransfer
# Register your models here.

admin.site.register(Wallet)
admin.site.register(WalletEntry)
admin.site.register(WalletTransfer)

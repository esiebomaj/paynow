from django.contrib import admin
from wallets.models import Wallet, WalletEntry, WalletTransfer
# Register your models here.

class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')

class WalletEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'entry_type', "reference")

class WalletTransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'amount', "status")

admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletEntry, WalletEntryAdmin)
admin.site.register(WalletTransfer, WalletTransferAdmin)

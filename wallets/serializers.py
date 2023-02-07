from rest_framework import serializers
from wallets.models import Wallet

class FundWalletSerializer(serializers.Serializer):
    wallet_id = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)


class VerifyFundWalletSerializer(serializers.Serializer):
    reference = serializers.CharField(required=True)


class WithdrawWalletSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)
    bank_account_id = serializers.CharField(required=True)
    entry_type = serializers.CharField(required=True)

class TransferWalletSerializer(serializers.Serializer):
    sender_id = serializers.CharField(required=True)
    recipient_username = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)


class WalletLogSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    reference = serializers.CharField(required=True)
    entry_type = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


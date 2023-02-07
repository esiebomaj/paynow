from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from wallets.service import WalletService, WalletEntryTypes
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# topup flow
# frontend calls us 
# we initialize payment with ext payment service
# create a payment model
# return payment auth url

class FundWalletViewSet(ViewSet):
    """
    {
    "wallet_id": 2,
    "amount": 50000
    }
    """
    @action(detail=False, methods=['post'])
    def init(self, request):
        res =  WalletService().init_fund_wallet(data=request.data)
        return Response(res)

    @action(detail=False, methods=['post'])
    def complete(self, request):
        res =  WalletService().verify_fund_wallet(data=request.data)
        return Response(res)


class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = {**request.data, "entry_type": WalletEntryTypes.WITHDRAWAL, "user_id": request.user.id}
        res =  WalletService().withdraw(data=data)
        return Response(res)


class TransferView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        res =  WalletService().transfer(data=request.data)
        return Response(res)


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from payments.service import PaymentService
from rest_framework.permissions import IsAuthenticated
from payments.serializers import PaymentSerializer


# Create your views here.

class BankListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        rs = PaymentService().get_list_of_banks()
        return Response(rs)

class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        rs = PaymentService().list(user_id=request.user.id)
        serializer = PaymentSerializer(rs, many=True)
        return Response(serializer.data)

class PaymentWebhook(APIView):
    def post(self, request):
        rs = PaymentService().acknoledge_webhook(request.data)
        return Response(rs)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.service import BankAccountService
from rest_framework.permissions import IsAuthenticated


# {
# "user": 2,
# "account_number": "0063612599",
# "account_name": "Esieboma Jeremiah",
# "bank_name": "Access Bank",
# "bank_code": "044"
# }


class CreateBankAccountView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = {**request.data, "user": request.user.id}
        res = BankAccountService().create(data)
        return Response(res)
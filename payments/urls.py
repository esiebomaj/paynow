
from django.contrib import admin
from django.urls import path, include
from payments.views import BankListView, PaymentWebhook, TransactionListView

urlpatterns = [
    path('list_of_banks/', BankListView.as_view()),
    path('transactions/', TransactionListView.as_view()),
    path('payment_webhook/', PaymentWebhook.as_view())
]
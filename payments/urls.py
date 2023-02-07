
from django.contrib import admin
from django.urls import path, include
from payments.views import BankListView, PaymentWebhook

urlpatterns = [
    path('list_of_banks/', BankListView.as_view()),
    path('payment_webhook/', PaymentWebhook.as_view())
]
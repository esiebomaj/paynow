
from django.contrib import admin
from django.urls import path, include
from ussd.views import USSDCallbackView

urlpatterns = [
    path('', USSDCallbackView.as_view()),
]
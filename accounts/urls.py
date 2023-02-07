
from django.contrib import admin
from django.urls import path, include
from accounts.views import CreateBankAccountView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('create-bank-account/', CreateBankAccountView.as_view())
]
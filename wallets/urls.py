from rest_framework.routers import DefaultRouter
from wallets.views import FundWalletViewSet, WithdrawView, TransferView
from django.urls import path, include


router = DefaultRouter()
router.register(r'fund', FundWalletViewSet, basename='wallet')
urlpatterns = router.urls
urlpatterns += {
    path('withdraw/', WithdrawView.as_view()),
    path('transfer/', TransferView.as_view())
}
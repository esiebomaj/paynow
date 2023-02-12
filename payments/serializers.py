from payments.models import Payment
from rest_framework.serializers import ModelSerializer


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
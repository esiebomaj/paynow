# from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import  UserDetailsSerializer
# from dj_rest_auth.registration.views import RegisterView
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from accounts.models import Phone, BankAccount
from wallets.models import Wallet
from wallets.serializers import WalletSerializer
from django.db.transaction import atomic

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Phone

class CustomRegisterSerializer(RegisterSerializer):
    phone_number = serializers.CharField( max_length=20, min_length=5, required=True,)
    ext = serializers.CharField( max_length=5, min_length=1, required=True,)

    def validate_phone_number(self, phone_number):
        if phone_number[0] == "0":
            raise ValidationError("Remove trailing 0 (Zero)")
        
        # check exists
        if Phone.objects.filter(phone_number=phone_number, ext=self.initial_data.get("ext")).exists():
            raise ValidationError("phone number exists")
        return phone_number

    def custom_signup(self, request, user):
        with atomic():
            
            phone_number = str(request.data.get("phone_number"))
            ext = str(request.data.get("ext"))
            phone_with_ext = "+" + ext + phone_data

            phone_data = {  "user":user.id, 
                            "phone_number": phone_number,
                            "ext": ext,
                            "phone_with_ext": phone_with_ext }

            # create phone for user
            serializer = PhoneSerializer(data=phone_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # create wallet for user
            Wallet.objects.create(user_id=user.id)

            super().custom_signup(request, user)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = "__all__"

class CustomeUserSerializer(UserDetailsSerializer):
    def to_representation(self, instance):
        rt = super().to_representation(instance)
        phone = Phone.objects.filter(user_id=instance.id).first()
        wallet = Wallet.objects.filter(user_id=instance.id).first()
        accounts = BankAccount.objects.filter(user_id=instance.id)
        rt["phone"] = PhoneSerializer(instance=phone).data if phone else None
        rt["wallet"] = WalletSerializer(instance=wallet).data if wallet else None
        rt["bank_accounts"] = AccountSerializer(instance=accounts, many=True).data 
        return rt


from accounts.serializers import AccountSerializer
from accounts.models import BankAccount, User, Phone
from django.contrib.auth import authenticate, get_user_model


class BankAccountService():
    def create(self, data):
        serializer = AccountSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"message": "Bank account created successfully"}

    def retrieve(self, **kwargs):
        return BankAccount.objects.get(**kwargs)

class UserService():
    def retrieve(self, **kwargs):
        return User.objects.get(**kwargs)

    def retrieve_user_by_phone_with_ext(self, phone_with_ext):
        phone = Phone.objects.filter(phone_with_ext=phone_with_ext).first()
        if not phone:
            return None
        return phone.user

    def authenticate(self, username, password):
        return authenticate(request=None, username=username, password=password)

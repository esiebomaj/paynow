from accounts.serializers import AccountSerializer
from accounts.models import BankAccount, User

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

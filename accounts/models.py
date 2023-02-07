from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    USERNAME_FIELD="username"


class Phone(models.Model):
    ext = models.CharField(max_length=5, null=False, blank=False)
    phone_number =  models.CharField(max_length=20, null=False, blank=False)
    verified = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def create_phone(cls, data):
        cls.objects.create(**data)
    

class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number =  models.CharField(max_length=200, null=False, blank=False)
    account_name = models.CharField(max_length=200, null=False, blank=False)
    bank_name = models.CharField(max_length=200, null=False, blank=False)
    bank_code = models.CharField(max_length=200, null=False, blank=False)
    currency = models.CharField(max_length=200, default="NGN", null=False, blank=False)
    external_reciepient_id = models.CharField(max_length=200, null=True, blank=True)


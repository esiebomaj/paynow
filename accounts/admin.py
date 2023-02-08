from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Phone, BankAccount


class PhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', "ext", "phone_with_ext")

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account_number', "account_name", "bank_name", "bank_code", "currency", "external_reciepient_id")

admin.site.register(User, UserAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
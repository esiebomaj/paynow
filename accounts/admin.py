from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Phone, BankAccount

admin.site.register(User, UserAdmin)
admin.site.register(Phone)
admin.site.register(BankAccount)
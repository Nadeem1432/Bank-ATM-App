from django.contrib import admin
from .models import ATMAccount
# Register your models here.
@admin.register(ATMAccount)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'balance','pin']
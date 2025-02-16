# atm/serializers.py
from rest_framework import serializers
from .models import ATMAccount

class ATMAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ATMAccount
        fields = ['account_number', 'pin', 'balance']
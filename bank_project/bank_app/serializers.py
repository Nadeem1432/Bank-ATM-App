# bank/serializers.py
from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'email', 'account_number', 'password', 'pin', 'balance']

    def create(self, validated_data):
        validated_data['username'] = validated_data.get('account_number')
        validated_data['first_name'] = validated_data.get('name')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('account_number', instance.account_number)
        instance.first_name = validated_data.get('name', instance.first_name)
        return super().update(instance, validated_data)
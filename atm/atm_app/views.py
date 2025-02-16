# atm/views.py
import pika
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ATMAccount
from decimal import Decimal
class WithdrawMoneyView(APIView):
    def post(self, request):
        account_number = request.data.get('account_number')
        pin = request.data.get('pin')
        amount = Decimal(request.data.get('amount'))

        try:
            atm_account = ATMAccount.objects.get(account_number=account_number, pin=pin)
            if atm_account.balance >= amount:
                atm_account.balance -= amount
                atm_account.save()
                self.send_to_bank(atm_account, -amount)
                return Response({"message": "Withdrawal successful", "remaining_balance": atm_account.balance}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
        except ATMAccount.DoesNotExist:
            return Response({"error": "Invalid account number or PIN"}, status=status.HTTP_400_BAD_REQUEST)

    def send_to_bank(self, atm_account, amount):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='transaction')
        message = {
            'account_number': atm_account.account_number,
            'amount': str(amount)
        }
        channel.basic_publish(exchange='', routing_key='transaction', body=json.dumps(message))
        connection.close()

class DepositMoneyView(APIView):
    from decimal import Decimal
    def post(self, request):
        account_number = request.data.get('account_number')
        pin = request.data.get('pin')
        amount = Decimal(request.data.get('amount'))

        try:
            atm_account = ATMAccount.objects.get(account_number=account_number, pin=pin)
            atm_account.balance += amount
            atm_account.save()
            self.send_to_bank(atm_account, amount)
            return Response({"message": "Deposit successful", "updated_balance": atm_account.balance}, status=status.HTTP_200_OK)
        except ATMAccount.DoesNotExist:
            return Response({"error": "Invalid account number or PIN"}, status=status.HTTP_400_BAD_REQUEST)

    def send_to_bank(self, atm_account, amount):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='transaction')
        message = {
            'account_number': atm_account.account_number,
            'amount': str(amount)
        }
        channel.basic_publish(exchange='', routing_key='transaction', body=json.dumps(message))
        connection.close()

class CheckBalanceView(APIView):
    def get(self, request):
        account_number = request.data.get('account_number')
        pin = request.data.get('pin')
        try:
            atm_account = ATMAccount.objects.get(account_number=account_number, pin=pin)
            return Response({"Current balance": atm_account.balance}, status=status.HTTP_200_OK)
        except ATMAccount.DoesNotExist:
            return Response({"error": "Invalid account number or PIN"}, status=status.HTTP_400_BAD_REQUEST)
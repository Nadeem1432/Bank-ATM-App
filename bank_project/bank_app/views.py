# bank/views.py
import pika
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account
from .serializers import AccountSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class CreateAccountView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            try:
                self.send_to_atm(account)
            except Exception as e:
                return Response({"error": "An error occurred while creating ATM account"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            refresh = RefreshToken.for_user(account)
        
            return Response({"account_number": account.account_number,
                              "pin": account.pin,
                              "token": str(refresh.access_token),
                              'message': 'Account created.'
                              }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_to_atm(self, account):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='account_creation')
        message = {
            'account_number': account.account_number,
            'pin': account.pin,
            'balance': str(account.balance)
        }
        channel.basic_publish(exchange='', routing_key='account_creation', body=json.dumps(message))
        connection.close()

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        account_number = request.data.get('account_number')
        password = request.data.get('password')
        try:
            account = Account.objects.get(account_number=account_number, password=password)
            refresh = RefreshToken.for_user(account)
        
            return Response({
                              "access_token": str(refresh.access_token),
                              "Account Holder Name": account.first_name,
                              "Account Holder Email": account.email,
                              "account_number": account.account_number,
                              "balance": account.balance,
                              'message': 'Login successfully.'
                              }, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class ViewAccountView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            return Response({"name": request.user.first_name,
                              "balance": request.user.balance,
                              "account_number": request.user.account_number}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
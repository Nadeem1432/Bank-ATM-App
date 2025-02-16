# atm/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('withdraw/', WithdrawMoneyView.as_view(), name='withdraw'),
    path('deposit/', DepositMoneyView.as_view(), name='deposit'),
    path('check-balance/', CheckBalanceView.as_view(), name='check-balance'),
]
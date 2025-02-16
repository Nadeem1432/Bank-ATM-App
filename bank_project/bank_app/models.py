# bank/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    account_number = models.CharField(max_length=20, unique=True)
    pin = models.CharField(max_length=4)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.account_number

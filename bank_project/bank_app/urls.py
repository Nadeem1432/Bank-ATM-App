# bank/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('create-account/', CreateAccountView.as_view(), name='create-account'),
    path('login/', LoginView.as_view(), name='login'),
    path('view-account/', ViewAccountView.as_view(), name='view-account'),
]
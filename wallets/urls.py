from django.urls import path
from wallets.views import *



urlpatterns = [
    path('', wallet, name="wallet"),
    
]
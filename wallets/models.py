from django.db import models
from django.db.models import Max
from auctions.models import User
from django.db import models



class Wallet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	address = models.CharField(max_length = 200, blank=True, null=True)
	amount = models.DecimalField(max_length = 200, blank=True, null=True, max_digits=10000, decimal_places=10) 
	password = models.CharField(max_length = 200, blank=True, null=True)  
# Create your models here.

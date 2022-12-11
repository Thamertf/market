from django import forms
from django.forms import ModelForm
from django.db import models
from .models import *
from django.db.models import Model

class SendMoneroForm(forms.ModelForm):
	class Meta:
		model = Wallet
		fields = ['user', 'address', 'amount', 'password']
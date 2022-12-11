
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import *
from django import forms
from .models import User
from .models import *	


class ActiveListingForm(forms.ModelForm):
	class Meta:
		model = ActiveListing
		fields = ['title', 'shortDescription', 'category', 'image', 'price', 'description', 'expires']
		
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']

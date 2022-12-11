from django.db.models.signals import post_save
from .models import User
from django.contrib.auth.models import Group
from .models import Account

def user_account(sender, instance, created, **kwargs):
	if created:
		Account.objects.create(user=instance)
		print('profile created!')
post_save.connect(user_account, sender=User)
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from datetime import timedelta, timezone
from django.utils import timezone
from math import ceil
from django.utils.text import slugify


class User(AbstractUser):
    is_merchant = models.BooleanField('Is merchant', default=False)
    is_support = models.BooleanField('Is support', default=False)



class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    email = models.CharField(max_length = 200, blank=True, null=True)
    account_pic = models.ImageField(default="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/495px-No-Image-Placeholder.svg.png", null=True, blank=True)
    balance = models.FloatField(default=0.00)
    date_created = models.DateTimeField(auto_now_add = True, null = True)


    def __str__(self):
        return self.user.username






class Category(models.Model):

    name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True, blank=True, null=True)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)





class ActiveListing(models.Model):
    class Meta:
        verbose_name_plural = 'Active Listing'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    shortDescription = models.CharField(max_length=125)
    description = models.CharField(max_length=356)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(max_length=500, default='https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/495px-No-Image-Placeholder.svg.png', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    date_added = models.DateTimeField(null=True)
    expires =  models.DateTimeField(auto_now=False, null=True)


    def __str__(self):
        return self.title




class WatchList(models.Model):
    class Meta:
        verbose_name_plural = 'Watch list'

    user = models.CharField(max_length=64)
    items = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)


class Comments(models.Model):
    class Meta:
        verbose_name_plural = 'Comments'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)
    comment = models.TextField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now=True)


class Bids(models.Model):
    class Meta:
        verbose_name_plural = 'Bids'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now=True)


    
class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'transaction_buyer')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'transaction_reciever')
    amount = models.FloatField()
    timestamp = models.DateField(auto_now=True)
    item = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)
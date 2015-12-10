from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, email, name, password):
        user = self.model(
            email=email,
            name=name,
            created_at=timezone.now()
        )
        user.set_password(password)
        #setattr(user, 'name', name)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Customer(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    #password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    # the model must know how to identify the user
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customers'


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order')
    product = models.ForeignKey('Product')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'orderitems'


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer)
    fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    fulfilled_at = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'orders'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(blank=True, null=True)
    rating = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=4096, blank=True, null=True)
    rating = models.IntegerField()
    product = models.ForeignKey(Product)
    customer = models.ForeignKey(Customer)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'reviews'



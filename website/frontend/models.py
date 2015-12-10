# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

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

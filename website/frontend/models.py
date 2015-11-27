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


class Categories(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'categories'


class Customers(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'customers'


class Orderitems(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey('Orders')
    product = models.ForeignKey('Products')
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'orderitems'


class Orders(models.Model):
    id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customers)
    fulfilled = models.IntegerField()
    created_at = models.DateTimeField()
    fulfilled_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Products(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey(Categories, blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock_quantity = models.IntegerField(blank=True, null=True)
    rating = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'products'


class Reviews(models.Model):
    id = models.IntegerField(primary_key=True)
    comment = models.CharField(max_length=4096, blank=True, null=True)
    rating = models.IntegerField()
    product = models.ForeignKey(Products)
    customer = models.ForeignKey(Customers)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reviews'

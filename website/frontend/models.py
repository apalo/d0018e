from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models, transaction
from django.utils import timezone


class CheckoutNotCompleted(Exception):
    pass


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
    updated_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'orderitems'

    @property
    def total_price(self):
        if self.order.fulfilled:
            return self.price * self.quantity
        return self.product.price * self.quantity


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer)
    fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    fulfilled_at = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'orders'

    @property
    def total_price(self):
        if self.fulfilled:
            return self.price
        _price = 0
        for orderitem in self.orderitem_set.all():
            _price += orderitem.total_price
        return _price

    @classmethod
    def update_shopping_basket(cls, updated_qty, order):
        for orderitem in order.orderitem_set.all():
            qty = int(updated_qty.get("quantity-%s" % orderitem.product.id, 0))
            if not qty or qty <= 0:
                orderitem.delete()
                continue
            orderitem.quantity = min(qty, orderitem.product.stock_quantity)
            orderitem.save()

    @classmethod
    def fulfil(cls, updated_qty, order):
        # lock products
        price = 0
        valid = True
        with transaction.atomic():
            products = Product.objects.select_for_update().filter(id__in=map(lambda o: o.product_id, order.orderitem_set.all()))
            orderitems = order.orderitem_set.all()
            for orderitem in orderitems:
                qty = int(updated_qty.get("quantity-%s" % orderitem.product.id, 0))
                if not qty or qty <= 0 or qty > orderitem.product.stock_quantity:
                    valid = False
                    continue
                orderitem.quantity = qty
                orderitem.price = orderitem.product.price
                orderitem.product.stock_quantity = models.F("stock_quantity") - orderitem.quantity
                price += orderitem.price * orderitem.quantity

            if valid:
                for oi in orderitems:
                    oi.product.save()
                    oi.save()
                order.price = price
                order.fulfilled = True
                order.fulfilled_at = datetime.now()
                order.save()
                return True
            return False


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(blank=True, null=True)
    rating = models.FloatField()

    @property
    def in_stock(self):
        return self.stock_quantity > 0

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



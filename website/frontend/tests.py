from django.test import TestCase, TransactionTestCase
from django.db import transaction
from django.utils import timezone

from .models import Product, Category, Customer, Order, OrderItem

class ProductTests(TestCase):
    def test_products_count(self):
        product = Product.objects.create(name="Netty in Action", price=350.99, stock_quantity=15, rating=0)
        self.assertEquals(Product.objects.count() == 1, True)

    def test_products_created(self):
        Product.objects.create(name="Go in Action", price=350.99, stock_quantity=15, rating=0)

        product = Product.objects.first()
        self.assertEquals(product.name, "Go in Action")

class CategoryTests(TestCase):
    def test_category_count(self):
        category = Category.objects.create(name="Books")
        self.assertEquals(Category.objects.count() == 1, True)

    def test_category_retreive(self):
        Category.objects.create(name="Laptops")
        category = Category.objects.get(name="Laptops")
        self.assertEquals(category.name, "Laptops")

class CustomerTests(TestCase):
    def test_customer_crated(self):
        Customer.objects.create(email="fake@ltu.local", password="bcrypt?", name="Fake User")
        customer = Customer.objects.first()
        self.assertEquals(customer.name, "Fake User")

class OrderTests(TransactionTestCase):
    def test_product_added_to_basket(self):
        customer = Customer.objects.create(email="fake@ltu.local", password="bcrypt?", name="Fake User")
        product = Product.objects.create(name="Netty in Action", price=350.99, stock_quantity=15, rating=0)

        # order / shopping basket
        order = Order.objects.create(customer=customer)
        order.orderitem_set.create(product=product)
        #order.save()

        self.assertEquals(order.orderitem_set.count > 0, True)

    def test_checkout_from_baset(self):
        customer = Customer.objects.create(email="fake@ltu.local", password="bcrypt?", name="Fake User")
        product = Product.objects.create(name="Netty in Action", price=350.99, stock_quantity=15, rating=0)

        order = Order.objects.create(customer=customer)
        order_item = order.orderitem_set.create(product=product, quantity=1)
        
        product_quantity = product.stock_quantity

        form_data = {
            "quantity-%s" % product.id: 3
        }

        Order.fulfil(form_data, order)

        order.refresh_from_db()
        product.refresh_from_db()
        for orderitem in order.orderitem_set.all():
            self.assertEquals(orderitem.quantity, 3)
        self.assertEquals(order.fulfilled, True)
        self.assertEquals(product.stock_quantity, 12)


    def test_invalid_checkout_from_baset(self):
        customer = Customer.objects.create(email="fake@ltu.local", password="bcrypt?", name="Fake User")
        product = Product.objects.create(name="Netty in Action", price=350.99, stock_quantity=15, rating=0)

        order = Order.objects.create(customer=customer)
        order_item = order.orderitem_set.create(product=product, quantity=1)
        
        product_quantity = product.stock_quantity

        form_data = {
            "quantity-%s" % product.id: 30
        }

        Order.fulfil(form_data, order)

        order.refresh_from_db()
        product.refresh_from_db()
        for orderitem in order.orderitem_set.all():
            self.assertEquals(orderitem.quantity, 1)
        self.assertEquals(order.fulfilled, False)
        self.assertEquals(product.stock_quantity, 15)
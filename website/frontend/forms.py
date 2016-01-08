from django.forms import ModelForm
from .models import Customer, Category, Product

class RegistrationForm(ModelForm):

	class Meta:
		model = Customer
		fields = ['email','name','password']

class AdminCategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = ["name"]

class AdminProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ["name", "category", "price", "stock_quantity"]


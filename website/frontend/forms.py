from django.forms import ModelForm
from .models import Customers

class RegistrationForm(ModelForm):

	class Meta:
		model = Customers
		fields = ['email','name','password']

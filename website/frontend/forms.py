from django.forms import ModelForm
from .models import Customer

class RegistrationForm(ModelForm):

	class Meta:
		model = Customer
		fields = ['email','name','password']

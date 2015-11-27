from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Categories, Products

def index(request):
    category_list = Categories.objects.all()
    product_list = Products.objects.all()
    template = loader.get_template('frontend/index.html')
    context = RequestContext(request, {
        'product_list':product_list,
        'category_list':category_list,
    })
    return HttpResponse(template.render(context))

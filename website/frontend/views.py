from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from .models import Category, Product

def index(request):
    category_list = Category.objects.all()
    product_list = Product.objects.all()
    template = loader.get_template('frontend/index.html')
    context = RequestContext(request, {
        'product_list':product_list,
        'category_list':category_list,
    })
    return HttpResponse(template.render(context))

def product_details(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Products doesn't exists")
    return render(request, "frontend/product_details.html", {"product": product})

def products_buy(request, product_id):
    # TODO: check if user is logged in, otherwise redirect back or something
    pass # TODO: implement adding to basket to the logged in user
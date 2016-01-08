from django.shortcuts import render, render_to_response, redirect, Http404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Avg, Count
from .models import Category, Product, Order, Review, Customer
from .forms import RegistrationForm, AdminCategoryForm, AdminProductForm
from django.utils import timezone

def index(request):
    return render(request, "dashboard/index.html")

def products_index(request):
    products = Product.objects.all()
    return render(request, "dashboard/products.html", {"products": products})

def products_new(request):
    if request.method == "POST":
        product = Product()
        form = AdminProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.rating = 0
            product.save()
            return redirect("/dashboard/products/%s/edit/" % product.id)
    else:
        form = AdminProductForm()

    return render(request, "dashboard/product_form.html", {"form": form})

def products_edit(request, product_id):
    if request.method == "POST":
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=product_id)
            form = AdminProductForm(request.POST, instance=product)
            if form.is_valid():
                product = form.save()
                return redirect("/dashboard/products/%s/edit/" % product.id)
    else:
        product=Product.objects.get(pk=product_id)
        form = AdminProductForm(instance=product)

    return render(request, "dashboard/product_form.html", {"form": form})

def categories_index(request):
    categories = Category.objects.all()
    return render(request, "dashboard/categories.html", {"categories": categories})

def categories_new(request):
    if request.method == "POST":
        category = Category()
        form = AdminCategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect("/dashboard/categories/%s/edit/" % category.id)
    else:
        form = AdminCategoryForm()

    return render(request, "dashboard/category_form.html", {"form": form})

def categories_edit(request, category_id):
    if request.method == "POST":
        category = Category.objects.get(pk=category_id)
        form = AdminCategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect("/dashboard/categories/%s/edit/" % category.id)
    else:
        category=Category.objects.get(pk=category_id)
        form = AdminCategoryForm(instance=category)

    return render(request, "dashboard/category_form.html", {"form": form})
from django.shortcuts import render, render_to_response, redirect, Http404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Avg, Count
from .models import Category, Product, Order, Review, Customer
from .forms import RegistrationForm
from django.utils import timezone

def category_reqctx(request):
    return {
        "global_categories": Category.objects.all()
    }

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
    reviews = Review.objects.filter(product__id = product_id)
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Products doesn't exists")
    return render(request, "frontend/product_details.html", {"product": product, "reviews": reviews})

@login_required
def products_buy(request, product_id):
    order, _ = Order.objects.get_or_create(customer=request.user, fulfilled=False)
    product = Product.objects.get(pk=product_id)
    # if the product exists in the order, update with current value+1
    if not product.stock_quantity:
        return redirect("/products/%s/?maxqty=0" % product.id)
    orderitem, created = order.orderitem_set.update_or_create(product=product)
    if not created:
        if orderitem.quantity >= product.stock_quantity:
            return redirect("/products/%s/?maxqty=1" % product.id)
        orderitem.quantity = F("quantity")+1
        orderitem.save()
    return redirect("/order/")
    

def login_view(request):
    error_msg = ''
    uname = ''
    passw = ''
    if request.POST:
        # get login information from HTML form
        uname = request.POST['username']
        passw = request.POST['password']
        user = authenticate(username=uname, password=passw)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                error_msg = "User is not active"
        else:
            error_msg = "Incorrect e-mail or password"
    return render(request, "frontend/login.html", {'error': error_msg})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def register_view(request):
    template = loader.get_template('frontend/register.html')
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = get_user_model().objects.create_user(
                email = request.POST['email'],
                name = request.POST['name'],
                password = request.POST['password']
            )
            return redirect('reg_complete')
    else:
        form = RegistrationForm()
    context = RequestContext(request, {'form': form})
    return HttpResponse(template.render(context))


def reg_complete_view(request):
    template = loader.get_template('frontend/reg_complete.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def category_view(request, cat_name = None):
    template = loader.get_template('frontend/category.html')
    filtered_category = Category.objects.get(name=cat_name)
    category_id = filtered_category.id
    product_list = [p for p in Product.objects.all() if p.category_id == category_id]
    context = RequestContext(request, {
        'product_list': product_list,
        'category_name': cat_name,
        'category_id': category_id,
    })
    return HttpResponse(template.render(context))

def review(request, product_id):
    error = ""
    if request.method == 'POST':
        with transaction.atomic():
            comment = request.POST['comment']
            try:
                rating = request.POST['rating']
                product = Product.objects.select_for_update().get(pk=product_id)
                customer = Customer.objects.get(pk=request.user.id)
                review_obj = Review(
                        comment=comment, 
                        rating=rating,
                        product=product,
                        customer=customer,
                        created_at=timezone.now())
                aggrating = Review.objects.filter(product_id=product.id).aggregate(avg_rating=Avg("rating"), review_count=Count("id"))
                if aggrating.get("avg_rating"):
                    product.rating = (aggrating.get("avg_rating") * aggrating.get("review_count") + int(review_obj.rating))/(aggrating.get("review_count")+1)
                else:
                    product.rating = review_obj.rating
                product.save()
                review_obj.save()
                return render(request, "frontend/review_complete.html")
            except KeyError:
                # exception if no 'rating' exists in POST
                error = "You must provide a product rating."
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    # Each user may only review a product once
    review_exists = False
    if request.user.is_authenticated():
        r = Review.objects.filter(customer=request.user.id).filter(product=product_id)
        if r:
            review_exists = True
    return render(request, "frontend/review.html", {"product": product, "review_exists": review_exists, "error": error})


# shopping basket
@login_required
def shopping_basket(request):
    try:
        order = Order.objects.get(customer=request.user, fulfilled=False)
        if request.method == "POST":
            with transaction.atomic():
                if request.POST.get("order") == "Update":
                    Order.update_shopping_basket(request.POST, order)
                    return redirect("/order/")
                elif request.POST.get("order") == "Checkout":
                    status = Order.fulfil(request.POST, order)
                    if status:
                        return redirect("/orders/%s/" % order.id)
                    return redirect("/order/?qty=1")
    except Exception as e:
        print e
        order = None

    return render(request, "frontend/shopping_basket.html", {"order": order})

@login_required
def order_details(request, order_id):
    order = Order.objects.get(pk=order_id)
    if not (order.customer_id == request.user.id or order.fulfilled):
        return redirect("/order/")
    return render(request, "frontend/order_details.html", {"order": order})


@login_required
def orders(request):
    orders = Order.objects.filter(customer=request.user, fulfilled=True).order_by("-id")
    return render(request, "frontend/orders.html", {"orders": orders})

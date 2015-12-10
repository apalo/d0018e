from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^reg_complete/$', views.reg_complete_view, name='reg_complete'),
    url(r'^category/laptops/$', views.category_view, {'cat_name':'laptops'}, name='category'),
    url(r'^category/desktops/$', views.category_view, {'cat_name':'desktops'}, name='category'),
    url(r'^category/monitors/$', views.category_view, {'cat_name':'monitors'}, name='category'),
    url(r'^category/keyboards/$', views.category_view, {'cat_name':'keyboards'}, name='category'),
    url(r'^category/mice/$', views.category_view, {'cat_name':'mice'}, name='category'),
    url(r'^category/books/$', views.category_view, {'cat_name':'books'}, name='category'),
    url(r'^products/(?P<product_id>\d+)/$', views.product_details, name="products.details"),
    url(r'^products/(?P<product_id>\d+)/add/$', views.products_buy, name="products.buy"),
]
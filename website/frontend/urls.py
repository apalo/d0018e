from django.conf.urls import url
from . import views, admin_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^reg_complete/$', views.reg_complete_view, name='reg_complete'),
    url(r'^category/(?P<cat_name>\w+)/$', views.category_view, name='category'),
    url(r'^products/(?P<product_id>\d+)/$', views.product_details, name="products.details"),
    url(r'^products/(?P<product_id>\d+)/add/$', views.products_buy, name="products.buy"),
	url(r'^review/(?P<product_id>\d+)/$', views.review, name="review"),
    url(r'^order/$', views.shopping_basket, name="shopping_basket"),
    url(r'^account/orders/$', views.orders, name="orders"),
    url(r'^orders/(?P<order_id>\d+)/$', views.order_details, name="order.details"),
    url(r'^dashboard/$', admin_views.index, name="dashboard.index"),
    url(r'^dashboard/products/$', admin_views.products_index, name="dashboard.products"),
    url(r'^dashboard/products/new/$', admin_views.products_new, name="dashboard.products_new"),
    url(r'^dashboard/products/(?P<product_id>\d+)/edit/$', admin_views.products_edit, name="dashboard.products_edit"),
    url(r'^dashboard/categories/$', admin_views.categories_index, name="dashboard.categories"),
    url(r'^dashboard/categories/new/$', admin_views.categories_new, name="dashboard.categories_new"),
    url(r'^dashboard/categories/(?P<category_id>\d+)/edit/$', admin_views.categories_edit, name="dashboard.categories_edit"),
]
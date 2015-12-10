from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^reg_complete/$', views.reg_complete_view, name='reg_complete'),
    url(r'^category/(?P<cat_name>\w+)/$', views.category_view, name='category'),
    url(r'^products/(?P<product_id>\d+)/$', views.product_details, name="products.details"),
    url(r'^products/(?P<product_id>\d+)/add/$', views.products_buy, name="products.buy"),
]
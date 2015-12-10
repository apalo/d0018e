from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/(?P<product_id>\d+)/$', views.product_details, name="products.details"),
    url(r'^products/(?P<product_id>\d+)/add/$', views.products_buy, name="products.buy"),
]

from django.contrib import admin
from django.urls import path
from goods import views

app_name='goods'

urlpatterns = [
    path('', views.catalog,name='index'),
    path('category/<slug:category_name>/',views.catalog,name='category'),
    path ('product/<slug:product_slug>/',views.product,name='product'), 
]

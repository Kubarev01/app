from unicodedata import category
from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render
from traitlets import default

from goods.models import Products
from goods.utils import q_search

# Create your views here.


def catalog(request,category_slug=None):

    page= request.GET.get('page', 1) #получить page если нет значения то 1
    on_sale= request.GET.get('on_sale',None)
    order_by= request.GET.get('order_by',None)
    query = request.GET.get('q',None)

    if category_slug == 'all':
         goods= Products.objects.all()
    elif query:
         goods = q_search(query)
    else:
         goods=get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
         goods = goods.filter(discount__gt=0)
    if order_by and order_by != "default":
         goods = goods.order_by(order_by)
   
    paginator= Paginator(goods, 3)  # выводит по три товара на стр
    current_page = paginator.page(int(page)) #номер страницы
    context = {
        "title": "Home - каталог",
        "goods": current_page, #возвращает query-set урезанный до 3
        "slug_url": category_slug
        #"filtered": filtered
        
    }
    return render(request, "goods/catalog.html",context)


def product(request, product_slug):

    product=Products.objects.get(slug=product_slug)

    context = {
        'product':product
    }

    return render(request, "goods/product.html",context)


    



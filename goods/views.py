from itertools import product
from typing import Any
from unicodedata import category
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.db.models.base import Model as Model
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.template.base import kwarg_re

from django.utils.cache import get_conditional_response
from django.views.generic import DetailView, ListView
from traitlets import default

from goods.models import Products
from goods.utils import q_search

# Create your views here.


class CatalogView(ListView):
     model=Products
     template_name='goods/catalog.html'
     context_object_name='goods'
     paginate_by=3

     def get_queryset(self) -> QuerySet[Any]:
          category_slug=self.kwargs.get('category_slug')
          on_sale=self.request.GET.get('on_sale')
          query=self.request.GET.get('q')
          order_by=self.request.GET.get('order_by')


          if category_slug == 'all':
               goods= super().get_queryset()
          elif query:
               goods = q_search(query)
          else:
               goods=super().get_queryset().filter(category__slug=category_slug)
               if not goods.exists():
                    raise Http404()

          if on_sale:
               goods = goods.filter(discount__gt=0)
          if order_by and order_by != "default":
               goods = goods.order_by(order_by)
          return goods
     

     def get_context_data(self, **kwargs) -> dict[str, Any]:
         context = super().get_context_data(**kwargs)
         context["title"] = 'Home - каталог'
         context['slug_url']= self.kwargs.get('category_slug')
         return context
     


# def catalog(request,category_slug=None):

#     page= request.GET.get('page', 1) #получить page если нет значения то 1
#     on_sale= request.GET.get('on_sale',None)
#     order_by= request.GET.get('order_by',None)
#     query = request.GET.get('q',None)

#     if category_slug == 'all':
#          goods= Products.objects.all()
#     elif query:
#          goods = q_search(query)
#     else:
#          goods=get_list_or_404(Products.objects.filter(category__slug=category_slug))

#     if on_sale:
#          goods = goods.filter(discount__gt=0)
#     if order_by and order_by != "default":
#          goods = goods.order_by(order_by)
   
#     paginator= Paginator(goods, 3)  # выводит по три товара на стр
#     current_page = paginator.page(int(page)) #номер страницы
#     context = {
#         "title": "Home - каталог",
#         "goods": current_page, #возвращает query-set урезанный до 3
#         "slug_url": category_slug
#         #"filtered": filtered
        
#     }
#     return render(request, "goods/catalog.html",context)






# def product(request, product_slug):

#     product=Products.objects.get(slug=product_slug)

#     context = {
#         'product':product
#     }

#     return render(request, "goods/product.html",context)


class ProductView(DetailView):
     template_name="goods/product.html"
     slug_url_kwarg='product_slug'

     #из функции get_object вернется обьект с именем object, но мы можем его переименовать
     context_object_name='product'

     def get_object(self, queryset: QuerySet[Any] | None = ...):
          
          product=Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
          return product
     
     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
          context=super().get_context_data(**kwargs)
     
          context['title']=self.object.name
          return context
     



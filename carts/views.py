import re
from urllib import response
from django.contrib import sessions
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View
from carts.mixins import CartMixin
from carts.models import Cart
from carts.templatetags.carts_tags import user_carts
from carts.utils import get_user_carts
from goods.models import Products



class CartAddView(CartMixin,View):

    def post(self,request):
        product_id=request.POST.get('product_id')
        product= Products.objects.get(id=product_id)

        cart=self.get_cart(request,product=product)

        if cart:
            cart.quantity+=1
            cart.save()

        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None, 
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                product=product,quantity=1)

        response_data={
            "message":"Товар добавлен в корзину",
            #передаем для перерисовки новую разметку сод корзины
            "cart_items_html":self.render_cart(request)
    
        }

        return JsonResponse(response_data)

# Create your views here.
# def cart_add(request):

#     product_id= request.POST.get("product_id")
#     product= Products.objects.get(id=product_id)
    
#     if request.user.is_authenticated:
#         carts=Cart.objects.filter(user=request.user, product=product)
    
#         if carts.exists():
#             cart=carts.first()
#             if cart:
#                 cart.quantity+=1
#                 cart.save()

#         else:
#             Cart.objects.create(user=request.user,product=product,quantity=1)
    
#     else:
#         carts= Cart.objects.filter(session_key=request.session.session_key,
#                                    product=product)

#         if carts.exists():
#             cart=carts.first()
#             if cart:
#                 cart.quantity+=1
#                 cart.save()

#         else:
#             Cart.objects.create(session_key=request.session.session_key,product=product,quantity=1)

#     user_cart= get_user_carts(request)
#     cart_items_html= render_to_string(
#         "carts/includes/included_cart.html",{"carts":user_cart}, request=request
#     )


#     response_data={
#         "message":"Товар добавлен в корзину",
#         #передаем для перерисовки новую разметку сод корзины
#         "cart_items_html":cart_items_html
        

#     }


#     return JsonResponse(response_data)
    

class CartRemoveView(CartMixin,View):

    def post(self,request):
        cart_id=request.POST.get("cart_id")

        
        cart=self.get_cart(request,cart_id=cart_id)
       
        quantity=cart.quantity

        cart.delete()

    
        response_data={
            "message":"Товары удалены из корзины",
            #передаем для перерисовки новую разметку сод корзины
            "cart_items_html":self.render_cart(request),
            "quantity_deleted": quantity,
        }

        return JsonResponse(response_data)


# def cart_remove(request):
#     cart_id=request.POST.get("cart_id")

    
#     cart=Cart.objects.get(id=cart_id)

#     quantity=cart.quantity
#     cart.delete()

#     user_cart= get_user_carts(request)
#     cart_items_html= render_to_string(
#         "carts/includes/included_cart.html",{"carts":user_cart}, request=request
#     )


#     response_data={
#         "message":"Товары удалены из корзины",
#         #передаем для перерисовки новую разметку сод корзины
#         "cart_items_html":cart_items_html,
#         "quantity_deleted": quantity,
#     }

#     return JsonResponse(response_data)





class CartChangeView(CartMixin,View):
    def post(self,request):
        cart_id=request.POST.get("cart_id")
        quantity= request.POST.get("quantity")

        cart=self.get_cart(request,cart_id=cart_id)

        cart.quantity=quantity
        cart.save()

       

        updated_quantity = cart.quantity

        

        response_data={
            "message":"Колличество товаров изменено",
            #передаем для перерисовки новую разметку сод корзины
            "cart_items_html":self.render_cart(request),
            "quantity": updated_quantity,
        }

        return JsonResponse(response_data)
 

# def cart_change(request):
#     cart_id=request.POST.get("cart_id")
#     quantity= request.POST.get("quantity")

#     cart=Cart.objects.get(id=cart_id)

#     cart.quantity=quantity
#     cart.save()
#     updated_quantity = cart.quantity

#     user_cart= get_user_carts(request)
#     cart_items_html= render_to_string(
#         "carts/includes/included_cart.html",{"carts":user_cart}, request=request
#     )


#     response_data={
#         "message":"Колличество товаров изменено",
#         #передаем для перерисовки новую разметку сод корзины
#         "cart_items_html":cart_items_html,
#         "quantity": updated_quantity,
#     }

#     return JsonResponse(response_data)
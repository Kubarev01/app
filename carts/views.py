from urllib import response
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from carts.models import Cart
from carts.templatetags.carts_tags import user_carts
from carts.utils import get_user_carts
from goods.models import Products


# Create your views here.
def cart_add(request):

    product_id= request.POST.get("product_id")
    product= Products.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        carts=Cart.objects.filter(user=request.user, product=product)
    
        if carts.exists():
            cart=carts.first()
            if cart:
                cart.quantity+=1
                cart.save()

        else:
            Cart.objects.create(user=request.user,product=product,quantity=1)
    
    user_cart= get_user_carts(request)
    cart_items_html= render_to_string(
        "carts/includes/included_cart.html",{"carts":user_cart}, request=request
    )


    response_data={
        "message":"Товар добавлен в корзину",
        #передаем для перерисовки новую разметку сод корзины
        "cart_items_html":cart_items_html

    }


    return JsonResponse(response_data)
    

def cart_remove(request):
    cart=Cart.objects.get(id=cart_id)
    cart.delete()
     #Возвращает на ту же страницу где и был пользователь      
    return redirect(request.META['HTTP_REFERER'])

def cart_change(request,product_id):
    ...
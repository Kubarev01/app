from email import message
from importlib.metadata import requires
from math import log
from urllib import request
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from carts.models import Cart
from orders.forms import CreateOrder
from orders.models import Order, OrderItem
from orders.queries import CreateOrderQuery

# Create your views here.

class CreateOrderView(LoginRequiredMixin, FormView):
    template_name='orders/create_order.html'
    form_class=CreateOrder
    success_url=reverse_lazy('main:index')

    def form_valid(self, form):
        return CreateOrderQuery(self,form)
    
    def form_invalid(self, form):
        messages.success(request,str(form.errors))
        return redirect('orders:create_order')    
    

    def get_initial(self):
        initial=super().get_initial()
        initial={
            'first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name,
        }
    
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titile'] = 'Home - Оформление заказа'
        context['order'] = True
        return context
    


# @login_required()
# def create_order(request):
#     if request.method=='POST':
#         form=CreateOrder(data=request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user=request.user

#                     cart_items=Cart.objects.filter(user=user)
                
#                     if cart_items.exists():
#                         #Создать заказ
#                         order= Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data['phone_number'],
#                             requires_delivery=form.cleaned_data['requires_delivery'],
#                             delivery_address=form.cleaned_data['delivery_address'],
#                             payment_on_get=form.cleaned_data['payment_on_get'],
#                         )

#                         #Создать заказанные товары
#                         for cart_item in cart_items:
#                             product= cart_item.product
#                             name= cart_item.product.name
#                             price=cart_item.product.display_discounted_price()
#                             quantity= cart_item.quantity

                      

#                             if product.quantity < quantity:
#                                 raise ValidationError(f'Недостаточное колличество товара {name} на складе\
#                                                       В наличии {product.quantity}')


#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                                 )
                            
#                             #вычитаем заказанные товары
#                             product.quantity-=quantity
#                             product.save()

#                             #Очищаем корзину после заказа:
#                         cart_items.delete()

#                         messages.success(request,'Заказ оформлен!')
                            
#                         return redirect('user:profile')
                            


#             except ValidationError as e:
#                 messages.success(request,str(e))
#                 return redirect('orders:create_order')


           
#     else:
#         initial={
#             'first_name':request.user.first_name,
#             'last_name':request.user.last_name,
#         }

#         form = CreateOrder(initial=initial)

#     context={
#         'title':"HOME - оформление заказа",
#         'form':form,
#         'order': True
#     } 

#     return render(request,"orders/create_order.html",context=context)

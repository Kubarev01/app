
from urllib import request



from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect

from carts.models import Cart
from orders.models import Order, OrderItem




def CreateOrderQuery(self,form):
            try:
                with transaction.atomic():
                    user=self.request.user

                    cart_items=Cart.objects.filter(user=user)
                
                    if cart_items.exists():
                        #Создать заказ
                        order= Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )

                        #Создать заказанные товары
                        for cart_item in cart_items:
                            product= cart_item.product
                            name= cart_item.product.name
                            price=cart_item.product.display_discounted_price()
                            quantity= cart_item.quantity

                      

                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное колличество товара {name} на складе\
                                                      В наличии {product.quantity}')


                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                                )
                            
                            #вычитаем заказанные товары
                            product.quantity-=quantity
                            product.save()

                            #Очищаем корзину после заказа:
                        cart_items.delete()

                        messages.success(self.request,'Заказ оформлен!')
                            
                        return redirect('user:profile')
                            


            except ValidationError as e:
                messages.success(self.request,str(e))
                return redirect('orders:create_order')

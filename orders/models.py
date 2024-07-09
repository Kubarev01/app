from django.db import models
from django.forms import CharField

from goods.models import Products
from users.models import User

# Create your models here.


class OrderitemQueryset(models.QuerySet):
     
    def total_price(self):
        return sum(cart.product_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0




class Order(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.SET_DEFAULT,blank=True,null=True,default=None,verbose_name="Пользователь")
    created_timestamp=models.DateTimeField(auto_now_add=True,verbose_name='Время создания заказа')
    phone_number=models.CharField(max_length=20,verbose_name='Номер телефона')
    requires_delivery=models.BooleanField(default=False,verbose_name='Требуется доставка')
    delivery_address=models.CharField(null=True,blank=True,verbose_name='Адрес доставки')
    payment_on_get=models.BooleanField(default=False,verbose_name='Оплата при получении')
    is_paid=models.BooleanField(default=False,verbose_name='Оплачено')
    status=models.CharField(max_length=50,default="В обработке", verbose_name='Статус заказа')

    class Meta():
        db_table='order'
        verbose_name='Заказ'
        verbose_name_plural='Заказы'

    def __str__(self):
        return f"Заказ №{self.pk} | Покупатель: {self.user.first_name} {self.user.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order,on_delete=models.CASCADE,default=None,null=True,verbose_name='Заказ')
    product = models.ForeignKey(to=Products,on_delete=models.SET_DEFAULT,null=True,default=None,verbose_name='Товар')
    name = models.CharField(max_length=150,verbose_name='Название')
    price = models.DecimalField(max_digits=7,decimal_places=2,verbose_name='Цена')
    quantity=models.PositiveIntegerField(default=0,verbose_name='Колличество')
    created_timestamp=models.DateTimeField(auto_now_add=True,verbose_name='Время продажи')

    class Meta():
        db_table='order_item'
        verbose_name='Проданный товар'
        verbose_name_plural='Проданные товары'

    objects= OrderitemQueryset.as_manager()

    
    def __str__(self):
        return f"Товар :{self.name} | Заказ №{self.order.pk}"
    
    def products_price(self):
        return f'{round(self.price*self.quantity,2)}'
    
    
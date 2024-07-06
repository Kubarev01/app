
from django.contrib import sessions
from django.db import models

from goods.models import Products
from users.models import User

# Create your models here.
class CartQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.product_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0
    
    
class Cart(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Пользователь')
    product =models.ForeignKey(to=Products,on_delete=models.CASCADE,verbose_name='Товар')
    quantity=models.PositiveSmallIntegerField(default=0,verbose_name='Колличество')
    session_key=models.CharField(max_length=32,null=True,blank=True)
    created_timestap=models.DateTimeField(auto_now_add=True,verbose_name='Дата добавления')
    
   

    #Переопределяем менеджер objetcs
    objects= CartQueryset().as_manager()


    class Meta():
        db_table='cart'
        verbose_name='Корзина'
        verbose_name_plural='Корзина'

    def __str__(self):
        if self.user:
            return f'Пользователь {self.user.username} | Товар {self.product.name} | Колличество {self.quantity}'
        return f'Анонимный пользователь | Товар {self.product.name} | Колличество {self.quantity}'

    def product_price(self):
        return round(self.product.display_discounted_price()*self.quantity,2)
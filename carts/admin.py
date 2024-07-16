from re import search
from django.contrib import admin

from carts.models import Cart

# Register your models here.

class CartTabAdmin(admin.TabularInline):
    #указываем модель привязки
    model=Cart
    fields=["product","quantity","created_timestap"]
    search_fields=["product","quantity","created_timestap"]
    #запрет на изменение времени

    readonly_fields=("created_timestap",)
    #одно своводное поле для добавления корзины
    extra=1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=["user","product_display","quantity","created_timestap"]
    list_filter= ["created_timestap","user","product__name","quantity"]


    def product_display(self,obj):
        return f"{obj.product.name}"
    
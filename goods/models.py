from gc import DEBUG_COLLECTABLE
from re import S
from tabnanny import verbose
from django.db import models

# Create your models here.

class Categories(models.Model):
    name= models.CharField(max_length=150,unique=True,verbose_name='Название')
    slug=models.SlugField(max_length=200, unique=True,blank=True,null=True,verbose_name='URL')
    
    class Meta:
        db_table='category'
        verbose_name='Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'

class Products(models.Model):
    name= models.CharField(max_length=150,unique=True,verbose_name='Название')
    slug=models.SlugField(max_length=200, unique=True,blank=True,null=True,verbose_name='URL')
    description=models.TextField(blank=True,null=True,verbose_name='Описание')
    image=models.ImageField(upload_to='goods_images',blank=True,null=True,verbose_name='Изображение')
    price=models.DecimalField(default=0.00,max_digits=7,decimal_places=2,verbose_name='Цена')
    discount=models.DecimalField(default=0.00,max_digits=7,decimal_places=2,verbose_name='Скидка в %')
    quantity=models.PositiveIntegerField(default=0,verbose_name='Колличество')
    category=models.ForeignKey(to=Categories,on_delete=models.CASCADE,verbose_name='Категория')

    class Meta:
        db_table='product'
        verbose_name='Продукт'
        verbose_name_plural='Продукты'
        ordering = ("id",)
 
    def __str__(self):
        return f'{self.name} Колличество -{self.quantity}'
    
    #метод добавляющий нули в начало до 5-ти символов(00007)
    def display_id(self):
        return f"{self.id:05}"
    
    def display_discounted_price(self):
        if self.discount:
            return round(float(self.price)-(float(self.price)*float(self.discount)*0.01))
        
        return self.price
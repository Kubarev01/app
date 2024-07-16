from re import search
from django.contrib import admin
from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin
from users.models import User
# Register your models here.




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=["display_root_as_adm","first_name","last_name","email",]
    search_fields=["display_root_as_adm","first_name","last_name","email",]
    inlines=[CartTabAdmin,OrderTabulareAdmin]

    def display_root_as_adm(self,obj):
        if obj.username =="root":
            return f"Администратор"
        else:
            return obj.username
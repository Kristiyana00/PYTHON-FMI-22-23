from django.contrib import admin
from .models import MenuItem, Category, OrderModel
from restaurant.models import Restaurant, Menu

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Restaurant)
admin.site.register(Menu)
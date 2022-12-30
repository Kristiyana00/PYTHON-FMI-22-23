from django.db import models
from customer.models import MenuItem, OrderModel
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='restaurant-logos/', blank=True)

    def __str__(self):
        return "%s" % self.name


class Menu(models.Model):
    menu_name = models.CharField(max_length=50, blank=True)
    restaurant = models.OneToOneField(Restaurant, on_delete = models.CASCADE,primary_key=True,)
    menu_items = models.ManyToManyField(MenuItem)
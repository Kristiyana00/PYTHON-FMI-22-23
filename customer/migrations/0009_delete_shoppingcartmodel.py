# Generated by Django 4.1.4 on 2022-12-28 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_rename_shoppingcart_shoppingcartmodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShoppingCartModel',
        ),
    ]
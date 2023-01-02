# Generated by Django 4.1.4 on 2023-01-02 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_ordermodel_restaurant_id'),
        ('restaurant', '0003_restaurant_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_items',
            field=models.ManyToManyField(blank=True, to='customer.menuitem'),
        ),
    ]

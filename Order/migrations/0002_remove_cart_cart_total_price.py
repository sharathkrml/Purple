# Generated by Django 3.2.4 on 2021-07-21 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cart_total_price',
        ),
    ]

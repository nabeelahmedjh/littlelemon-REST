# Generated by Django 4.2.3 on 2023-07-25 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0002_rename_cart_usercart'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserCart',
        ),
    ]

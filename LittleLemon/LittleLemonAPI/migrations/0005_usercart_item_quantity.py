# Generated by Django 4.2.3 on 2023-07-25 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0004_usercart'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercart',
            name='item_quantity',
            field=models.SmallIntegerField(null=True),
        ),
    ]

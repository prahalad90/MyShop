# Generated by Django 4.2.5 on 2024-02-26 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_order_order_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_no',
            field=models.IntegerField(default=1000000, unique=True),
        ),
    ]

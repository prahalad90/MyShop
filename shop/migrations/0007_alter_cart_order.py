# Generated by Django 4.2.5 on 2024-01-23 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='order',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
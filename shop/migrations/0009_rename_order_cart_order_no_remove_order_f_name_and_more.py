# Generated by Django 4.2.5 on 2024-02-03 03:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0008_order_razorpay_id_order_razorpay_signature'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='order',
            new_name='order_no',
        ),
        migrations.RemoveField(
            model_name='order',
            name='F_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='L_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='order',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
        migrations.RemoveField(
            model_name='order',
            name='totalPrice',
        ),
        migrations.AddField(
            model_name='order',
            name='orderValue',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='trackingcode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('F_name', models.CharField(max_length=50)),
                ('L_name', models.CharField(max_length=50)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('pincode', models.CharField(max_length=6)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=10)),
                ('trackingcode', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

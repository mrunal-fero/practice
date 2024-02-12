# Generated by Django 5.0.2 on 2024-02-08 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_customer_credits'),
        ('order', '0002_alter_item_item_number_alter_order_reference_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_customer', to='customer.customer'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderitems_item', to='order.item'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderitems_order', to='order.order'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
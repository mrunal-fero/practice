# Generated by Django 5.0.2 on 2024-02-08 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_customer_customer_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='credits',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
    ]

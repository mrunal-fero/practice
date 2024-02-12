# Generated by Django 5.0.2 on 2024-02-07 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_number',
            field=models.CharField(editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='reference_number',
            field=models.CharField(editable=False, max_length=50, unique=True),
        ),
    ]

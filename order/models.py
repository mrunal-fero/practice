from django.db import models
from customer.models import Customer

import string, random

# Create your models here.
ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Unassigned', 'Unassigned'),
    ]
class Item(models.Model):
    item_number = models.CharField(max_length=50, editable=False, unique=True)
    description = models.CharField(max_length = 512)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)
    quantity = models.PositiveIntegerField(null = True)
    
    def save(self, *args, **kwargs):
        if not self.item_number:
            last_code = Item.objects.order_by('-id').first()
            if last_code:
                last_numeric_code = int(last_code.item_number.split('_')[1])
                self.item_number = f"{self.generate_random_string()}_{last_numeric_code + 1}"
            else:
                self.item_number = f"{self.generate_random_string()}_1000"
        super().save(*args, **kwargs)

    def generate_random_string(self, length=6):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.SET_NULL, null = True, related_name = "order_customer")
    reference_number = models.CharField(max_length=50, editable=False, unique=True)
    delivery_date = models.DateField()
    customer_name = models.CharField(max_length = 32)
    address = models.TextField()
    coordinates = models.FloatField()
    amount = models.DecimalField (max_digits = 10, decimal_places = 2, null = True)
    is_cancelled = models.BooleanField(default = False)
    order_status = models.CharField(max_length = 20, choices = ORDER_STATUS_CHOICES, null = True)
    order_warning = models.CharField(max_length = 50, null = True)
    created_ts = models.DateTimeField(auto_now_add = True)
    updated_ts = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = self.generate_random_string()
        super().save(*args, **kwargs)

    def generate_random_string(self, length=11):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

class OrderItems(models.Model):
    item = models.ForeignKey(Item,on_delete = models.SET_NULL, null = True, related_name = "orderitems_item")
    order = models.ForeignKey(Order,on_delete = models.SET_NULL, null = True, related_name = "orderitems_order")
    quantity = models.IntegerField(null = True)

class OrderAttachment(models.Model):
    file = models.FileField(upload_to="media")
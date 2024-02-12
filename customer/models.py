from django.db import models

# Create your models here.

class Customer(models.Model):
    customer_code = models.CharField(max_length=50, editable=False, unique=True)
    customer_name = models.CharField(max_length = 32)
    address = models.TextField()
    coordinates = models.FloatField()
    credits = models.DecimalField(max_digits = 10, decimal_places = 2, default = 100)

    def save(self, *args, **kwargs):
        if not self.customer_code:
            last_code = Customer.objects.order_by('-id').first()
            if last_code:
                last_numeric_code = int(last_code.customer_code.split('_')[1])
                self.customer_code = f"{self.customer_name}_{last_numeric_code + 1}"
            else:
                self.customer_code = f"{self.customer_name}_1000"
        super().save(*args, **kwargs)


####
"""
customer credit
item qty validation
order cancellation using custom action in viewset
validations at serializer 
order attachmen (file field)
"""
from celery import shared_task, Celery
from .models import Order, OrderItems, Item
from customer.models import Customer
import json

celery = Celery()


@shared_task
def bulk_create_orders_and_items(data):
    orders_data = data
    for order_data in orders_data:
        customer = Customer.objects.get(customer_code=order_data['customer_code'])
        item = Item.objects.get(item_number=order_data['item_number'])

        is_older_order = Order.objects.filter(reference_number=order_data['reference_number']).exists()
        total_amount = item.price * order_data['quantity']

        if is_older_order:
            continue
        
        if item.quantity<order_data['quantity'] and customer.credits<total_amount:
            order_status = "Pending"
            order_warning = "Customer has unsufficient Credits and Items are Unsufficient"
            item_quantity = item.quantity
            customer_credits = customer.credits
        
        elif item.quantity<order_data['quantity']:
            order_status = "Pending"
            order_warning = "Item quantity is unsufficient"
            item_quantity = item.quantity
            customer_credits = customer.credits
        
        elif customer.credits<total_amount:
            order_status = "Pending"
            order_warning = "Customer has unsufficient Credits"
            item_quantity = item.quantity
            customer_credits = customer.credits
        
        else:
            order_status = "Unassigned"
            order_warning = "Everything is Good"
            item_quantity = item.quantity - order_data['quantity']
            customer_credits = customer.credits - total_amount

        order = Order.objects.create(
            reference_number=order_data['reference_number'],
            customer_name=customer.customer_name,
            delivery_date=order_data['date'],
            address=customer.address,
            coordinates=customer.coordinates,
            customer = customer,
            amount = total_amount,
            order_status=order_status,
            order_warning=order_warning
        )
        OrderItems.objects.create(
            order=order,
            item=item,
            quantity=order_data['quantity']
        )

        item.quantity = item_quantity
        item.save()

        customer.credits = customer_credits
        customer.save()
from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["address","customer_name","coordinates"]
        read_only_fields = ['id']

    # def validated_data(self):
    #     print("hi")
    #     customer_list = []
    #     for cust_obj in self.context.get('context'):
    #         customer = {
    #             "id":cust_obj.id,
    #             "customer_name":cust_obj.customer_name,
    #             "customer_code":cust_obj.customer_code,
    #             "address":cust_obj.address,
    #             "coordinates":cust_obj.coordinates
    #         }
    #         customer_list.append(customer)
    #     return customer_list

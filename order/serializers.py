from rest_framework import serializers
from .models import Item, OrderAttachment, Order

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ["item_number","description","price","quantity"]

class BulkDetailSerializer(serializers.Serializer):
    reference_number = serializers.CharField(max_length=50)
    item_number = serializers.CharField(max_length=50)
    quantity = serializers.IntegerField()
    customer_code = serializers.CharField(max_length=50)
    date = serializers.DateField()

class BulkUploadSerializer(serializers.Serializer):
    data = BulkDetailSerializer(many=True)

class OrderAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = OrderAttachment
        fields = ["file"]

class OrderCancelSerializer(serializers.ModelSerializer):
    is_cancelled = serializers.BooleanField(required = True)

    class Meta:
        model = Order
        fields = ["is_cancelled", "reference_number"]

class ImportFileSerializer(serializers.Serializer):
    file = serializers.FileField()
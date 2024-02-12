from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.decorators import action
from .models import Item, Order
from .task import bulk_create_orders_and_items
from .serializers import (
    ItemSerializer, 
    OrderCancelSerializer, 
    OrderAttachmentSerializer,
    ImportFileSerializer,
    BulkDetailSerializer
)
from customer.models import Customer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
import csv, io
from .renderer import CustomXLSXRenderer

# Create your views here.
class ItemViewSet(viewsets.ViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    # @extend_schema(
    #     responses=ItemSerializer
    # )
    def destroy(self, request, pk=None):
        queryset = self.queryset
        item = get_object_or_404(queryset, pk=pk)
        if item:
            item.delete()
        return Response({"message":"Deleted Successfully"})
    
    @extend_schema(
        responses=ItemSerializer,
        request=ItemSerializer
    )
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            item = Item.objects.create(**serializer.validated_data)
            response = {
                "id":item.id,
                "item_code":item.item_number,   
                "description":item.description,
                "quantity":item.quantity,
                "price":item.price
            }
        return Response(response)

    @extend_schema(
        responses=ItemSerializer
    )
    def retrieve(self, request, pk=None):
        queryset = self.queryset
        item = get_object_or_404(queryset, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    
    @extend_schema(
        responses=ItemSerializer,
        request=ItemSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        instance = kwargs.get('pk')
        item = get_object_or_404(self.queryset, pk=instance)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False,methods=['post'],serializer_class=ImportFileSerializer, parser_classes=[MultiPartParser])
    def item_import(self, request):
        if not 'file' in request.data:
            return Response({"message":"No file Uploaded"})

        serializer = ImportFileSerializer(data=request.data)
        if serializer.is_valid():
            file = request.data['file'].read()
            data = io.BytesIO(file)
            with open("tmp.csv", "wb") as csv_file:
                csv_file.write(data.getbuffer())
            
            with open("tmp.csv", "r", newline='', encoding='latin-1') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    try:
                        Item.objects.get(item_number=row[0])
                        continue
                    except:
                        Item.objects.create(
                            item_number = row[0],
                            description = row[1],
                            price = row[2],
                            quantity = row[3]
                        )
            return Response({"message":"File Uploaded"})
        else:
            return Response({"message":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], renderer_classes = [CustomXLSXRenderer])
    def export_item(self, request):

        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class BulkCreateViewSet(viewsets.ViewSet):
    serializer_class = BulkDetailSerializer(many=True)
    queryset = Order.objects.all()

    @action(detail = True, methods=['post'], serializer_class = OrderCancelSerializer)
    def cancel_order(self, request, pk=None):
        try:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=True):
                order = get_object_or_404(self.queryset, pk=pk)
                print(order)
                order.is_cancelled = True
                order.save()
                return Response({"message":"Done"})
            else:
                print("Hi")
                return Response(serializer.errors)

        except:
            return Response({"message":"Something Went Wrong"},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['post'], serializer_class = OrderAttachmentSerializer)
    def order_attachment(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"File Uploaded Successfully"})
        return Response(400,{"message":"Something Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['post'], serializer_class = BulkDetailSerializer(many=True))
    def bulk_order_create(self, request):
        try:
            data = request.data
            print(type(data))

            for order_data in data:

                try:
                    customer = Customer.objects.get(customer_code=order_data['customer_code'])
                except ObjectDoesNotExist:
                    return Response({"message":"Customer with this customer code '"+order_data['customer_code']+"' does not exist"}, status=status.HTTP_404_NOT_FOUND)

                try:
                    item = Item.objects.get(item_number=order_data['item_number'])
                except ObjectDoesNotExist:
                    return Response({"message":"Item with this item number '"+order_data['item_number']+"' does not exist"}, status=status.HTTP_404_NOT_FOUND)

                if not order_data['quantity']>0:
                    return Response({"message":"Quantity for Reference Number '"+order_data['reference_number']+"' should be greator than 0"}, status=status.HTTP_400_BAD_REQUEST)
            
            bulk_create_orders_and_items.delay(data)
            return Response({'message': 'Bulk creation task has been scheduled'})
        except:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class OrderAttachmentAPIVIew(generics.CreateAPIView):
    serializer_class = OrderAttachmentSerializer
    parser_classes = [MultiPartParser]

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"File Uploaded Successfully"})
        return Response(400,{"message":"Something Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)

class OrderCancelViewset(viewsets.ViewSet):
    serializer_class = OrderCancelSerializer
    queryset = Order.objects.all()

    @action(detail = True, methods=['post'])
    def cancel_order(self, request, pk=None):
        try:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=True):
                order = get_object_or_404(self.queryset, pk=pk)
                print(order)
                order.is_cancelled = True
                order.save()
                return Response({"message":"Done"})

        except:
            return Response({"message":"Something Went Wrong"},status=status.HTTP_400_BAD_REQUEST)

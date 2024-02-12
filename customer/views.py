from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from order.serializers import ImportFileSerializer
import io, csv
from rest_framework.parsers import MultiPartParser
from order.renderer import CustomXLSXRenderer
# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    def get_serializer_class(self):
        if self.action == 'import_customer':
            return ImportFileSerializer
        return CustomerSerializer

    # @extend_schema(
    #     responses=CustomerSerializer
    # )
    def destroy(self, request, pk=None):
        queryset = self.queryset
        customer = get_object_or_404(queryset, pk=pk)
        if customer:
            customer.delete()
        return Response({"message":"Deleted Successfully"})
    
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            customer = Customer.objects.create(**serializer.validated_data)
            response = {
                "id":customer.id,
                "customer_code":customer.customer_code,
                "address":customer.address,
                "coordinates":customer.coordinates
            }
        return Response(response)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        customer = get_object_or_404(queryset, pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail = False,methods=['post'], serializer_class = ImportFileSerializer, parser_classes = [MultiPartParser])
    def import_customer(self, request):
        if not 'file' in request.data:
            return Response({"message":"No file Uploaded"})

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = request.data['file'].read()
            data = io.BytesIO(file)
            with open("tmp.csv", "wb") as csv_file:
                csv_file.write(data.getbuffer())
            
            with open("tmp.csv", "r", newline='', encoding='latin-1') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    try:
                        Customer.objects.get(customer_code=row[0])
                        continue
                    except:
                        Customer.objects.create(
                            customer_code = row[0],
                            customer_name = row[1],
                            address = row[2],
                            coordinates = row[3]
                        )
            return Response({"message":"File Uploaded"})
        else:
            return Response(serializer.errors)
        
    @action(detail=False, methods=['get'], renderer_classes = [CustomXLSXRenderer])
    def export_customer(self, request):

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

         

from rest_framework import serializers
from ..models import Product, Order



class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"


class ProductBuySerializer(serializers.Serializer):
    product = serializers.ListField()
    quantity = serializers.ListField()

    class Meta:
        fields = ["product", "quantity"]    


class GenerateInvoiceSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=128)
    phone = serializers.CharField(max_length=10)
    address = serializers.CharField(max_length=1024)
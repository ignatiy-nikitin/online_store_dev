from products.models import Product
from rest_framework import serializers
from orders.models import Order, OrderFinal, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(source='order_items', many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderFinalSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
        
    class Meta:
        model = OrderFinal
        fields = '__all__'

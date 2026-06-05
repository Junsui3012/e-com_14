from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from apps.products.serializers import ProductListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    product_id = serializers.IntegerField(read_only=True)

    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fieds = ['id', 'items', 'total', 'total_items']

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_price', 'quantity', 'subtotal']
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'payment_status',
            'shipping_address', 'subtotal', 'shipping_cost', 'tax', 'total',
            'items', 'created_at'
        ]
        read_only_fields = ['id', 'order_number', 'status', 'payment_status', 'created_at']

class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.DictField()

    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_shipping_address(self, value):
        required_keys = ['street', 'city', 'state', 'zip_code', 'country']
        missing = [k for k in required_keys if not value.get(k)]

        if missing:
            raise serializers.ValidationError(f"Missing fields: {', '.join(missing)}")
        return value

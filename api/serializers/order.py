from order.models import Order, OrderDetails
from rest_framework import serializers
from menu.models import Menu
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
    def create(self, validated_data):
        return Order.objects.create(**validated_data)
    
class OrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetails
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def create(self, validated_data):
        return OrderDetails.objects.create(**validated_data)
    
class RatingOrderDetailsSerializer(serializers.ModelSerializer):
    productId = serializers.SerializerMethodField()
    class Meta:
        model = OrderDetails
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def create(self, validated_data):
        return OrderDetails.objects.create(**validated_data)
    
    def get_productId(self, obj):
        menu_id = Menu.objects.get(item_name=obj.itemName).id
        return menu_id
    
class CustomOrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetails
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    
class CustomOrderWithOrderDetailsSerializer(serializers.ModelSerializer):
    products = CustomOrderDetailsSerializer(source='orderdetails_set', many=True, read_only=True)
    class Meta:
        model = Order
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
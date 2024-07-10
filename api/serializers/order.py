from order.models import Order, OrderDetails
from rest_framework import serializers
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
    # bot = serializers.SerializerMethodField()
    # kot = serializers.SerializerMethodField()
    # tableNumber = serializers.SerializerMethodField()
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

    # def get_bot(self, obj):
    #     return int(obj.orderdetails_set.first().botID) if (obj.orderdetails_set.first() is not None and obj.orderdetails_set.first().botID is not None)else None
    
    # def get_kot(self, obj):
    #     return int(obj.orderdetails_set.first().kotID) if (obj.orderdetails_set.first() is not None and obj.orderdetails_set.first().kotID is not None) else None
    
    # def get_tableNumber(self, obj):
    #     return str(obj.table_no) if (obj.orderdetails_set.first() is not None and obj.table_no is not None) else None
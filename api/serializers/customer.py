from user.models import Customer
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
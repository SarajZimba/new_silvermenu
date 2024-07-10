from rest_framework.serializers import Serializer, ModelSerializer
from menu.models import Menu
from rest_framework import serializers

class MenuSerializerCreate(ModelSerializer):

    class Meta:
        model = Menu
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]


    def create(self, validated_data):
        return Menu.objects.create(**validated_data)
    
class MenuSerializerList(ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def get_image_url(self, obj):
        return str("api/" + obj.item_name)

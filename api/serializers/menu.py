from rest_framework.serializers import Serializer, ModelSerializer
from menu.models import Menu
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile

from menu.models import MenuType

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
        # image_bytes = validated_data.pop('image_bytes', None)
        # item_name = validated_data.get('item_name', None)
        return Menu.objects.create(**validated_data)

        # if image_bytes:
        #     menu.image_bytes = image_bytes
        #     menu.thumbnail = self.decode_image(image_bytes, item_name)
        #     menu.save()

        # return menu
    
    # def decode_image(self, image_bytes, item_name):
    #     try:
    #         decoded_img = base64.b64decode(image_bytes)

    #         image_file = ContentFile(decoded_img, name=f'{item_name}.jpg')
    #         return image_file
    #     except Exception as e:
    #         raise(e)


    
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

    
class MenuTypeSerializerList(ModelSerializer):
        products = MenuSerializerList(source='menu_set', many=True, read_only=True) 
        class Meta:       
            model = MenuType
            exclude = [
                "created_at",
                "updated_at",
                "status",
                "is_deleted",
                "sorting_order",
                "is_featured"
            ]


class MenuTypeSerializerListOutletWise(serializers.ModelSerializer):
    products = MenuSerializerList(many=True, read_only=True) 

    class Meta:
        model = MenuType
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Serialize the menus related to this MenuType
        menus = instance.menu_set.filter(outlet=self.context['outlet_name'])
        serialized_menus = MenuSerializerList(menus, many=True, context=self.context).data
        
        representation['products'] = serialized_menus
        
        return representation

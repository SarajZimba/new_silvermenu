from rest_framework.views import APIView
from rest_framework.response import Response
from menu.models import Menu
from api.serializers.menu import MenuSerializerCreate, MenuSerializerList

class MenuTypeWiseListView(APIView):
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')

        promotional_menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet_name, is_promotional=True)[:5]
        todayspecial_menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet_name, is_todayspecial=True)[:5]
        try:    
            promotional_serializer = MenuSerializerList(promotional_menus, many=True)
            todayspecial_serializer = MenuSerializerList(todayspecial_menus, many=True)
            data = {
                "promotional": promotional_serializer.data,
                "todayspecial": todayspecial_serializer.data
            }
            return Response(data, 200)

        except Exception as e:
            print(e)
            return Response("Something went wrong", 400)
        
class MenuListView(APIView):
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')

        menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet_name)
        # promotional_menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet_name, is_promotional=True)[:5]
        # todayspecial_menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet_name, is_todayspecial=True)[:5]
        try:    
            serializer = MenuSerializerList(menus, many=True)
            # todayspecial_serializer = MenuSerializerList(todayspecial_menus, many=True)
            data = serializer.data
            return Response(data, 200)

        except Exception as e:
            print(e)
            return Response("Something went wrong", 400)
        

class IsPromotional(APIView):
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')

        menus = Menu.objects.filter(status=True, is_deleted=False, is_promotional=True, outlet=outlet_name)

        try:
            serializer = MenuSerializerList(menus, many=True)
            data = serializer.data
            return Response(data, 200)

        except Exception as e:
            print(e)
            return Response("Something went wrong", 400)
        
class IsTodaySpecial(APIView):
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')

        menus = Menu.objects.filter(status=True, is_deleted=False, is_todayspecial=True, outlet=outlet_name)

        try:
            serializer = MenuSerializerList(menus, many=True)
            data = serializer.data
            return Response(data, 200)

        except Exception as e:
            print(e)
            return Response("Something went wrong", 400)



from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class MenuCreateAPIView(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        print(f"This is the {request.data}")
        datas = request.data  # Create a mutable copy of the request data
        outlet = kwargs.get('outlet_name')
        try:
            menus = Menu.objects.filter(status=True,is_deleted=False, outlet=outlet)
            menus.delete()
        except Exception as e:
            print(e)
        try:
            for data in datas:
                # data = data.copy()
                type = data.get('type', None)
                title = data.get('itemName', None)
                description = data.get('description', None)
                price = float(data.get('price', 0.0))
                group = data.get('group', None)
                image = data.get('image', None)  # Get the image from the request data
                image_bytes = data.get('image_bytes', None)
                discount_exempt = data.get('discountExempt', False)


                # Prepare the data for the serializer
                menu_data = {
                    'item_name': title,
                    'description': description,
                    'price': price,
                    'group': group,
                    'thumbnail': image,  # Add the image to the menu data
                    'discount_exempt':discount_exempt,
                    'type':type,
                    'outlet': outlet,
                    'image_bytes':image_bytes
                }
                
                print(f"This is the menu data {menu_data} ")

                serializer = MenuSerializerCreate(data=menu_data)
                if serializer.is_valid():
                    menu = serializer.save()
            return Response("menu Created", status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ImageByteView(APIView):
    def get(self, request, *args, **kwargs):
        menu_name = kwargs.get('menu_name')
        menu = Menu.objects.filter(item_name = menu_name).first()
        dict = {}
        if menu:
            dict = {
                'image': menu.image_bytes 
            }
        return Response(dict, 200)
    
class MenuSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        try:
            menus = Menu.objects.filter(item_name__icontains=keyword)
            serializer = MenuSerializerList(menus, many=True)            
            return Response(serializer.data, 200)
        except Exception as e:
            print(e)
            return Response("Some exception occured", 400)
        

class MenuPromotionalUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        outlet = kwargs.get('outlet_name')
        data = request.data
        item_name = data['item_name']

        try:
            menu = Menu.objects.get(item_name=item_name, outlet=outlet)
        except Exception as e:
            return Response("Something went wrong", 400)

        if menu.is_promotional == True:
            menu.is_promotional = False
            menu.save()

        if menu.is_promotional == False:
            menu.is_promotional = True
            menu.save()

        return Response("promotional type changed successfully", 200)
    
class MenuTodaySpecialUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        outlet = kwargs.get('outlet_name')
        data = request.data
        item_name = data['item_name']

        try:
            menu = Menu.objects.get(item_name=item_name, outlet=outlet)
        except Exception as e:
            return Response("Something went wrong", 400)

        if menu.is_todayspecial == True:
            menu.is_todayspecial = False
            menu.save()

        if menu.is_todayspecial == False:
            menu.is_todayspecial = True
            menu.save()

        return Response(" todayspecial type changed successfully", 200)

class MenuDetailView(APIView):
    def get(self, request, *args, **kwargs):
        menu_id = kwargs.get('menu_id')
        try:
            menu = Menu.objects.get(pk=menu_id)
        except Exception as e:
            return Response("Could not find the menu", 400)
        serializer = MenuSerializerList(menu)
        return Response(serializer.data, 200)            

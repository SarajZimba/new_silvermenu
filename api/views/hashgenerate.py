from rest_framework.views import APIView
from api.serializers.hashgenerate import HashValueSerializer
from rest_framework.response import Response
from order.models import HashValue

class HashAPIView(APIView):
    def post(self, request, *args, **kwargs):
        posted_data = request.data
        outlet = posted_data['outlet']
        table = posted_data['table']
        try:
            serializer = HashValueSerializer(data=posted_data)

            if serializer.is_valid():
                hashvalue_obj = HashValue.objects.filter(outlet=outlet, table=table)
                if hashvalue_obj:
                    hashvalue_obj.delete()
                hashvalue_obj = serializer.save()

                hashvalue = hashvalue_obj.hash_value

                return Response({"hashvalue": hashvalue}, 200)
            else:
                return Response(e, 400)
        except Exception as e:
            return Response(e, 400)        

class GiveTableOutletHashAPIView(APIView):
    def get(self, request, *args, **kwargs):
        hashvalue = kwargs.get('hashvalue')
        try:
            hashvalue_obj = HashValue.objects.get(hash_value=hashvalue)
            dict = {
                "outlet": hashvalue_obj.outlet, 
                "table_no": hashvalue_obj.table
            }
            return Response(dict, 200)
        except Exception as e:
            return Response(e, 400)
        
class ClearHashValue(APIView):
    def get(self, request, *args, **kwargs):
        hashvalue = kwargs.get('hashvalue')
        try:
            hashvalue_obj = HashValue.objects.get(hash_value=hashvalue)
            hashvalue_obj.delete()
            return Response("Hash object deleted successfully", 200)
        except Exception as e:
            return Response(e, 400)

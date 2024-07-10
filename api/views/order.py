from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.order import OrderDetailsSerializer,OrderSerializer, CustomOrderWithOrderDetailsSerializer
from django.db import transaction
from order.models import Order, OrderDetails
from django.utils import timezone

from rest_framework.permissions import AllowAny


class OrderCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None, *args, **kwargs):
        current_datetime = timezone.now()

        # Format the datetime as a string
        current_time_str = current_datetime.strftime('%H:%M')
        current_date_str = current_datetime.strftime('%Y-%m-%d')
        data = request.data
        data['state'] = "Pending"
        data['start_time'] = current_time_str
        data['date'] = current_date_str
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            order_details_data = request.data.get('order_details', [])

            for order_detail_data in order_details_data:
                order_detail_data['order'] = order.id
            order_details_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
            if order_details_serializer.is_valid():
                order_details_serializer.save()

                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                order.delete()
                return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, format=None):
        order_details_data = request.data

        for order_detail_data in order_details_data:
            order_id = order_detail_data.get('order')
            if not order_id:
                return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        order_details_serializer = OrderDetailsSerializer(data=request.data, many=True)
        
        if order_details_serializer.is_valid():
            with transaction.atomic():
                # Delete existing OrderDetails associated with the specified Order ID
                for order_detail_data in order_details_data:
                    OrderDetails.objects.filter(order=order_detail_data['order']).delete()

                # Save new OrderDetails
                order_details_serializer.save()
        
            future_order = Order.objects.filter(order=order_detail_data['order']).first()
            print(f"future_order {future_order}")
            future_order_data = []
            if future_order:
                for order_detail_data in order_details_data:
                    OrderDetails.objects.filter(order=future_order).delete()
                    print(f"This is the future order id {future_order.id}")
                    print()
                    order_detail_data['order'] = int(future_order.id)
                    future_order_data.append(order_detail_data)
                print(future_order_data)
                future_order_details_serializer = OrderDetailsSerializer(data=future_order_data, many=True)
                if future_order_details_serializer.is_valid():
                    future_order_details_serializer.save()
                else:
                    print("The data was not valid")

            return Response(order_details_serializer.data, status=status.HTTP_201_CREATED)
            
        else:
            return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class OrderListView(APIView):
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')
        orders = Order.objects.filter(outlet=outlet_name)

        serializer = CustomOrderWithOrderDetailsSerializer(orders, many=True)

        return Response(serializer.data, 200)

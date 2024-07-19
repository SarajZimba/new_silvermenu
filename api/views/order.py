from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.order import OrderDetailsSerializer,OrderSerializer, CustomOrderWithOrderDetailsSerializer
from django.db import transaction
from order.models import Order, OrderDetails
from django.utils import timezone
import pytz
from rest_framework.permissions import AllowAny
from django.db.models import Q
from order.utils import send_delivery_notification

class OrderCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None, *args, **kwargs):
        desired_timezone = pytz.timezone('Asia/Kathmandu')
        current_datetime = timezone.now().astimezone(desired_timezone)

        # Format the datetime as a string
        current_time_str = current_datetime.strftime('%I:%M %p')
        current_date_str = current_datetime.strftime('%Y-%m-%d')
        data = request.data
        data['state'] = "Pending"
        data['start_time'] = current_time_str
        data['date'] = current_date_str
        table_no = request.data['table_no']
        outlet_name = request.data['outlet']
        order_not_completed_in_table = Order.objects.filter(
            Q(table_no=table_no) & ~Q(state="Completed") &Q(outlet=outlet_name)
        ).order_by('id')

        if order_not_completed_in_table.exists():
            if order_not_completed_in_table.last().state == "Pending":
                order_details_data = request.data.get('order_details', [])

                for order_detail_data in order_details_data:
                    order_detail_data['order'] = order_not_completed_in_table.last().id
                order_details_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
                if order_details_serializer.is_valid():
                    order_details_serializer.save()

                    send_delivery_notification(outlet_name)

                    return Response(order_details_serializer.data, status=status.HTTP_201_CREATED)
                
                else:
                    # order.delete()
                    return Response(order_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            elif order_not_completed_in_table.last().state == "Accepted":             
                data['outlet_order'] = order_not_completed_in_table.last().outlet_order
                order_serializer = OrderSerializer(data=data)
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
        
        else:
            order_serializer = OrderSerializer(data=data)
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

            
        # return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
        orders = Order.objects.filter(outlet=outlet_name, state="Pending")

        serializer = CustomOrderWithOrderDetailsSerializer(orders, many=True)

        return Response(serializer.data, 200)
    
class OrderAcceptView(APIView):
    def get(self, request, *args, **kwargs):
        order = kwargs.get('order')
        outlet_order = kwargs.get('outlet_order')
        desired_timezone = pytz.timezone('Asia/Kathmandu')
        current_datetime = timezone.now().astimezone(desired_timezone)

        # Format the datetime as a string
        current_time_str = current_datetime.strftime('%I:%M %p')
        # current_date_str = current_datetime.strftime('%Y-%m-%d')
        order = Order.objects.get(id=order)
        order.accepted_time = current_time_str
        order.state = "Accepted"
        order.outlet_order = outlet_order
        order.save()
        return Response("Order time recorded")

from django.db.models import Sum
from decimal import Decimal
class OrderSessionTotal(APIView):
    def get(self, request, *args, **kwargs):
        outlet_name = kwargs.get('outlet_name')
        table_no = kwargs.get('table_no')
        # print(f'oulet_order {outlet_order}')
        orders = Order.objects.filter(Q(outlet=outlet_name) & Q(table_no=table_no) & ~Q(state="Completed") & ~Q(state="Cancelled"))
        # orders = Order.objects.filter(table_no=table_no)

        print(f'These are the orders {orders}')
        serializer = CustomOrderWithOrderDetailsSerializer(orders, many=True)

        total_inall_order_details = OrderDetails.objects.filter(order__in=orders).aggregate(total=Sum('total'))
        totalquantity_inall_order_details = OrderDetails.objects.filter(order__in=orders).aggregate(quantity=Sum('quantity'))
        print(totalquantity_inall_order_details)
        total_amount = total_inall_order_details['total'] if total_inall_order_details['total'] is not None else 0
        total_quantity = totalquantity_inall_order_details['quantity'] if totalquantity_inall_order_details['quantity'] is not None else 0
        total_items = OrderDetails.objects.filter(order__in=orders).count()
        vat = total_amount * Decimal(0.13)

        grand_total = total_amount + vat

        order_dict = {

            "orders" : serializer.data,
            "sub_total" : round(total_amount, 2),
            "vat" : round(vat, 2),
            "grand_total": round(grand_total, 2),
            "total_quantity": total_quantity,
            "total_items": total_items
    

        }

        return Response(order_dict, 200)


class CancelOrderAPIView(APIView):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            order = Order.objects.get(pk=order_id)
            order.state = "Cancelled"
            order.status = False
            order.save()
            return Response("Order cancelled successfully", 200)
        except Exception as e:
            return Response("No order found having that id", 400)






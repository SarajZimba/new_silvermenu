from django.db.models.signals import post_save
from user.models import UserLogin
from django.dispatch import receiver
from order.firebase import send_notification
from menu.models import FlagMenu
def send_delivery_notification(outlet, table_no):
    print("I am inside")

    table_no =table_no
    outlet=outlet
    active_users = UserLogin.objects.filter(outlet=outlet)
        
    if active_users:
        for user in active_users:
            token = user.device_token
            outlet = outlet if outlet else "" 

    

            final_msg = f"You have new items added to the order in table {table_no} "

            if token is not None or token != '':

                send_notification(token, "Order needs to be received", final_msg, {"item_added": "true"})

            else:
                print("The token is None")
    else:
        print(f"No active users in the outlet {outlet}")

import json
# from order.utils import is_update_pending
def send_order_notification(instance, state):
    print("I am inside")
    outlet=instance.outlet
    active_users = UserLogin.objects.filter(outlet=outlet)
    print(f"active users {active_users}")
    if active_users:
        for user in active_users:

            order_type = instance.type if instance.type else ""
            order_id = instance.id 
            table_no = instance.table_no if instance.table_no else ""
            dateTime = instance.start_time if instance.start_time else ""
            employee = instance.employee if instance.employee else ""
            noOfGuest = instance.noofguest if instance.noofguest else ""
            token = user.device_token
            outlet = instance.outlet if instance.outlet else "" 

            order_dict = {}
                            
            if order_type is not None:
                order_dict["orderType"] = order_type
                                
            if order_id is not None:
                order_dict["id"] = str(order_id)

            if table_no is not None:
                order_dict["tableNo"] = str(table_no)

            if dateTime is not None:
                order_dict["dateTime"] = dateTime

            if employee is not None:
                order_dict["Employee"] = employee

            if noOfGuest is not None:
                order_dict["noOfGuest"] = str(noOfGuest)

            if state == "Pending":
                flag = is_update_pending(instance)
                if flag == True:
                    order_dict["is_update"] = "true"
                else:
                    order_dict["is_update"] = "false"

            if state == "Accepted":
                order_dict["is_update"] = "true"

            if state == "Normal":
                order_dict["is_update"] = "false"
            flag = FlagMenu.objects.first().autoaccept_order
            if flag == True:
                order_dict["auto_accept"] = "true"
            if flag == False:
                order_dict["auto_accept"] = "false"

            order_dict["products"] = []
                            
            for order_details in instance.orderdetails_set.all():
            
                itemName = order_details.itemName if order_details.itemName else ""
                quantity = order_details.quantity if order_details.quantity else ""
                total = order_details.total if order_details.total else 0
                modification = order_details.modification if order_details.modification else ""                                
                products_dict = {}
                if itemName is not None:
                    products_dict['itemName'] = itemName
                if modification is not None: 
                    products_dict['modification'] = modification
                if quantity is not None: 
                    products_dict['quantity'] = quantity
                if total is not None:
                    products_dict['total'] = str(total)
                order_dict["products"].append(products_dict)
                            
            order_dict["products"] = json.dumps(order_dict["products"])

            final_msg = f"You have a new order in table {table_no}"

            print(token)
            if token is not None or token != '':
                print(f"before {order_dict}")
                send_notification(token, "Order needs to be received", final_msg, order_dict)
                print(f"after {order_dict}")
            else:
                print("The token is None")
    else:
        print(f"No active users in the outlet {outlet}")

from .models import Order, OrderDetails
def is_update_pending(order):
    # if order
    table_no= order.table_no
    outlet= order.outlet
    if Order.objects.filter(table_no=table_no, outlet=outlet, state='Accepted').exists():
        flag = True
    
    else:
        flag = False
    return flag
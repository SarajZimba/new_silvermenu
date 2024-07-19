from django.db import models
from alice_menu.utils import BaseModel
import json
# Create your models here.

class Order(BaseModel):
    employee = models.CharField(max_length=155, null=True)
    table_no = models.IntegerField(null=True)
    noofguest = models.IntegerField(null=True)
    start_time = models.CharField(max_length=255,null=True)
    end_time = models.CharField(max_length=255,null=True)
    type = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255, null=True)    
    discounts = models.CharField(max_length=255, null=True)
    date = models.DateField(null=True)
    barItem = models.CharField(max_length=10, null=True) 
    outlet = models.CharField(max_length = 100, null=True)
    accepted_time = models.CharField(max_length=100, null=True)
    outlet_order = models.IntegerField(null=True)


class OrderDetails(BaseModel):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=200, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currentState = models.CharField(max_length=20, null=True)
    quantity = models.IntegerField(null=True)
    modification = models.CharField(max_length=200, null=True)


from django.db.models.signals import post_save
from user.models import UserLogin
from django.dispatch import receiver
from .firebase import send_notification

@receiver(post_save, sender=Order)
def send_delivery_notification(sender, instance, created, **kwargs):
    print("I am inside")
    if created:
        outlet=instance.outlet
        active_users = UserLogin.objects.filter(outlet=outlet)
        
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

                order_dict["products"] = []
                            
                for order_details in instance.orderdetails_set.all():
            
                    itemName = order_details.itemName if order_details.itemName else ""
                    quantity = order_details.quantity if order_details.quantity else ""
                    total = order_details.total if order_details.total else 0
                                
                    products_dict = {}
                    if itemName is not None:
                        products_dict['itemName'] = itemName
                    if quantity is not None: 
                        products_dict['quantity'] = quantity
                    if total is not None:
                        products_dict['qty'] = str(total)
                    order_dict["products"].append(products_dict)
                            
                order_dict["products"] = json.dumps(order_dict["products"])

                final_msg = f"You have a new order "

                if token is not None or token != '':
                    print(f"before {order_dict}")
                    send_notification(token, "Order needs to be received", final_msg, order_dict)
                    print(f"after {order_dict}")
                else:
                    print("The token is None")
        else:
            print(f"No active users in the outlet {outlet}")
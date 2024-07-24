from django.db.models.signals import post_save
from user.models import UserLogin
from django.dispatch import receiver
from order.firebase import send_notification
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
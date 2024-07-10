from .models import Customer
def check_email(email):
    if Customer.objects.filter(email=email).exists():
        return True #means already email associated with another account
    else:
        return False 
    
from .models import Customer
def check_email_in_normal(email):
    if Customer.objects.filter(email=email).exists():
        return True #means already email associated with another account
    else:
        return False 
from django.db import models
from alice_menu.utils import BaseModel

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

class OrderDetails(BaseModel):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=200, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currentState = models.CharField(max_length=20, null=True)
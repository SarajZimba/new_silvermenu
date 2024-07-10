from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def HomeView(self):
    return HttpResponse("It is working")
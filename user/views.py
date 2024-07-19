from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.
def logout_user(request):
    logout(request)
    return redirect(reverse_lazy("user:login_view"))

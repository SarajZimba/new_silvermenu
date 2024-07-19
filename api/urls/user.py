# In urls.py
from django.urls import path
from api.views.user import UserLoginCreateAPIView

urlpatterns = [
    path('userlogin/', UserLoginCreateAPIView.as_view(), name='userlogin-create'),
    # Other paths for your application
]

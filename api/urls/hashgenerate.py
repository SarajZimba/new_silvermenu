from django.urls import path

from api.views.hashgenerate import HashAPIView, GiveTableOutletHashAPIView, ClearHashValue
urlpatterns = [
    path('create-hash/', HashAPIView.as_view(), name='create-hash'),
    path('get-outlettable-hash/<str:hashvalue>', GiveTableOutletHashAPIView.as_view(), name='get-outlettable-hash'),
    path('clear-hash/<str:hashvalue>', ClearHashValue.as_view(), name='clear-hash'),
    ]

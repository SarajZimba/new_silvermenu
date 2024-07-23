from django.urls import path

from api.views.bill_request import BillRequestAPIView, BillRequestListAPIView, BillRequestConfirmAPIView

urlpatterns = [
    path('bill-request/<str:outlet>', BillRequestAPIView.as_view(), name='bill-request'),
    path('bill-request-list/<str:outlet>', BillRequestListAPIView.as_view(), name='bill-request-list'),
    path('accept-billrequest/<int:billrequest_id>/', BillRequestConfirmAPIView.as_view(), name='billrequest-accept')
] 

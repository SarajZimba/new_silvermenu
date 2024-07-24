from django.urls import path

from api.views.order import OrderCreateAPIView, OrderListView, OrderAcceptView, CancelOrderAPIView

urlpatterns = [
    path('create-order/', OrderCreateAPIView.as_view(), name='create-order'),
    path('give-order/<str:outlet_name>', OrderListView.as_view(), name='give-order'),
    path('accept-order/<int:order>/<int:outlet_order>/', OrderAcceptView.as_view(), name='record-accept-time'),
    path('cancel-order/<int:order_id>/', CancelOrderAPIView.as_view(), name='cancel-order')
    # path('accept-order/<int:order>/', OrderAcceptView.as_view(), name='record-accept-time')
] 

from api.views.order import OrderSessionTotal
urlpatterns += [
    path('order-session/<str:outlet_name>/<int:table_no>/', OrderSessionTotal.as_view(), name='order-session'),
] 

from api.views.order import GiveItemsfromTable
urlpatterns += [
    path('table-items/<str:outlet_name>/<int:table_no>/', GiveItemsfromTable.as_view(), name='table-items'),
] 


from api.views.order import ReviewPending

urlpatterns += [
    path('is-pending/<str:outlet_name>/<int:table_no>/',ReviewPending.as_view(), name='is-session-comleted'),
] 
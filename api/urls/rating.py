from django.urls import path

from api.views.rating import RatingCreateAPIView

urlpatterns = [
    path('create-rating/', RatingCreateAPIView.as_view(), name='create-rating'),
    # path('give-order/<str:outlet_name>', OrderListView.as_view(), name='give-order'),
    # path('accept-order/<int:order>/<int:outlet_order>/', OrderAcceptView.as_view(), name='record-accept-time'),
    # path('cancel-order/<int:order_id>/', CancelOrderAPIView.as_view(), name='cancel-order')
    # path('accept-order/<int:order>/', OrderAcceptView.as_view(), name='record-accept-time')
] 
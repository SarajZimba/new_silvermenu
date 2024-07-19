from django.urls import path
from api.views.customer import CustomerNormalRegister, CustomerNormalLoginView, CustomerGuestLoginCreate, CustomerGoogleLoginView, CustomerGoogleRegister

urlpatterns = [
    path("customer-register/", CustomerNormalRegister.as_view(), name="customer-register"),
    path("customer-normal-login/", CustomerNormalLoginView.as_view(), name="customer-normal-login"),

]
urlpatterns += [
    path("customer-googleregister/", CustomerGoogleRegister.as_view(), name="customer-googleregister"),
    path("customer-google-login/", CustomerGoogleLoginView.as_view(), name="customer-google-login"),
]
urlpatterns += [
    path("customer-guest-login/", CustomerGuestLoginCreate.as_view(), name="customer-normal-login"),

]


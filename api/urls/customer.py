from django.urls import path
from api.views.customer import CustomerNormalRegister, CustomerNormalLoginView

urlpatterns = [
    path("customer-register/", CustomerNormalRegister.as_view(), name="customer-register"),
    path("customer-normal-login/", CustomerNormalLoginView.as_view(), name="customer-normal-login"),

]
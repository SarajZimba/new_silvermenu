from .order import urlpatterns as order_urlpatterns
# from .user import urlpatterns as user_urlpatterns
from .menu import urlpatterns as menu_urlpatterns
from .customer import urlpatterns as customer_urlpatterns
from .user import urlpatterns as user_urlpatterns
from .bill_request import urlpatterns as bill_request_urpatterns
from .rating import urlpatterns as rating_urlpatterns

urlpatterns = (
    []  + menu_urlpatterns + customer_urlpatterns + order_urlpatterns + user_urlpatterns + bill_request_urpatterns + rating_urlpatterns
)
from .order import urlpatterns as order_urlpatterns
# from .user import urlpatterns as user_urlpatterns
from .menu import urlpatterns as menu_urlpatterns
from .customer import urlpatterns as customer_urlpatterns

urlpatterns = (
    []  + menu_urlpatterns + customer_urlpatterns + order_urlpatterns #+ user_urlpatterns +
)
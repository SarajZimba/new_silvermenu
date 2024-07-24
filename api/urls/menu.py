from django.urls import path
from api.views.menu import MenuCreateAPIView, IsPromotional, MenuTypeProducts, ImageByteView, MenuListView, MenuTypeWiseListView, MenuSearchAPIView, MenuDetailView, MenuListViewAllOutlet

urlpatterns = [
    path("menu-create/<str:outlet_name>", MenuCreateAPIView.as_view(), name="menu-create"),
    path("menu-list/<str:outlet_name>", MenuListView.as_view(), name="menu-list"), 
    path("menu-list-alloutlet/", MenuListViewAllOutlet.as_view(), name="menu-list"), 
    path("menu-typewise-list/<str:outlet_name>", MenuTypeWiseListView.as_view(), name="menu-typewise-list"), 
    path("menu-type-products/<str:outlet_name>/<int:id>", MenuTypeProducts.as_view(), name="menu-type"),
    # path("menu-promotional/<str:outlet_name>/<int", IsPromotional.as_view(), name="menu-promotional"),
    path("images/<str:menu_name>", ImageByteView.as_view(), name="menu-imagebyte"),
    path("menu-detail/<int:menu_id>", MenuDetailView.as_view(), name="menu-detail"),

]

urlpatterns += [
    path("menu-search/", MenuSearchAPIView.as_view(), name="menu-search"),

]

from api.views.menu import MenuPromotionalUpdateAPIView, MenuTodaySpecialUpdateAPIView
urlpatterns += [
    path("update-todayspecial/<str:outlet_name>", MenuTodaySpecialUpdateAPIView.as_view(), name="update-todayspecial"),
    path("update-promotional/<str:outlet_name>", MenuPromotionalUpdateAPIView.as_view(), name="update-promotional"),

]

# Assuming you have an `api/` app or namespace for your API endpoints

from django.urls import path
from api.views.menu import FlagMenuToggleAPIView

urlpatterns += [
    path('flagmenu/toggle/', FlagMenuToggleAPIView.as_view(), name='flagmenu-toggle'),
]


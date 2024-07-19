
from django.urls import path
urlpatterns = []

from .views import MenuTypeList,MenuTypeDetail,MenuTypeCreate,MenuTypeUpdate,MenuTypeDelete

from .views import IndexView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]


urlpatterns += [
path('menu/type/', MenuTypeList.as_view(), name='menu_type_list'),
path('menu/type/<int:pk>/', MenuTypeDetail.as_view(), name='menu_type_detail'),
path('menu/type/create/', MenuTypeCreate.as_view(), name='menu_type_create'),
path('menu/type/<int:pk>/update/', MenuTypeUpdate.as_view(), name='menu_type_update'),
path('menu/type/delete', MenuTypeDelete.as_view(), name='menu_type_delete'),

]

from .views import MenuList,MenuDetail,MenuCreate,MenuUpdate,MenuDelete, MenuUpload
urlpatterns += [
path('menu/', MenuList.as_view(), name='menu_list'),
path('menu/<int:pk>/', MenuDetail.as_view(), name='menu_detail'),
path('menu/create/', MenuCreate.as_view(), name='menu_create'),
path('menu/<int:pk>/update/', MenuUpdate.as_view(), name='menu_update'),
path('menu/delete', MenuDelete.as_view(), name='menu_delete'),
path('menu/upload/', MenuUpload.as_view(), name='menu_upload'),

]
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from shop.views import *

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('',index,name='home'),
    path('product/<int:id>',productview,name="product"),
    path('search/',searchveiw,name='search'),
    path('add-to-cart/',add_to_cart,name='add-to-cart'),
    path('view-cart/',view_cart,name='cart'),
    path('remove-item/<int:id>',remove_item,name='remove'),
    path('less/<int:id>',less_qnt,name='less'),
    path('add/<int:id>',add_qnt,name ='add'),
    path('checkout/',checkout,name='checkout'),
    path('placeorder/',placeorder,name='placeorder'),
    path('continue/<str:trackingcode>',orderconfirm,name='confirm'),
    path('order',order),
    path('order/<int:id>',orderdetail,name='order'),
    path('logout',logoutview),
    path('login',loginview),
]
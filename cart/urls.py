
from . import views
from django.urls import path 

urlpatterns = [

    path("" , views.cart_summary , name='cart_summary'),
    path("add/" , views.cart_add , name='cart_add'),
    path("delete/" , views.cart_delete , name='cart_delete'),
    path("update/" , views.cart_update , name='cart_update')
]

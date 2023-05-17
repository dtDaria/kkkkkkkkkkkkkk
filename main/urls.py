from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', catalog, name='catalog'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('orders', order_list, name='orders'),
    path('orderCreate', order_view, name='order_create'),
    path('order_delete', delete_order, name='order_delete'),
    path('delete_order/<pk>', delete_order, name='delete_order'),
]
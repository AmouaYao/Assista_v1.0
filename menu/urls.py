from django.urls import path
from . import views

urlpatterns = [
    path('', views.splash_screen, name='splash_screen'),
    path('menu/', views.MenuOrderView, name='menu_order'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # if you have a home view
    path('restaurants/', views.restaurant_list, name='restaurant_list'),  # note the trailing slash
]
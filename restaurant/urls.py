from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path(
        'restaurant/<int:restaurant_id>/',
        views.restaurant_detail,
        name='restaurant_detail'
    ),
    path(
        'restaurant/<int:restaurant_id>/book/',
        views.book_restaurant,
        name='book_restaurant'
    ),
    path('register/', views.register, name='register'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path(
        'booking/<int:booking_id>/cancel/',
        views.cancel_booking,
        name='cancel_booking'
    ),
    path(
        'booking/<int:booking_id>/edit/',
        views.edit_booking,
        name='edit_booking'
    ),
    path(
        'booking/<int:booking_id>/delete/',
        views.delete_booking,
        name='delete_booking'
    ),
    path('contact/', views.contact, name='contact'),
    path('contact/messages/', views.contact_messages, name='contact_messages'),
    path('contact/<int:contact_id>/', views.view_contact, name='view_contact'),
    path('contact/<int:contact_id>/update-status/', views.update_contact_status, name='update_contact_status'),
    path('contact/<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),
    
    path('restaurant/<int:restaurant_id>/menu/', views.manage_menu, name='manage_menu'),
    path('restaurant/<int:restaurant_id>/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/<int:menu_item_id>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/<int:menu_item_id>/delete/', views.delete_menu_item, name='delete_menu_item'),
]

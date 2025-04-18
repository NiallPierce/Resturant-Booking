from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from booking import views as booking_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # For Allauth URLs
    path('', include('restaurant.urls')),  # Include restaurant URLs
    path('my-bookings/', booking_views.booking_list, name='booking_list'),
    path('my-bookings/<int:booking_id>/', booking_views.booking_detail, name='booking_detail'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
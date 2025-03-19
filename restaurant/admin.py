from django.contrib import admin
from .models import Restaurant, TimeSlot, Booking, MenuItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'opening_time', 'closing_time', 'capacity', 'contact_number')
    search_fields = ('name', 'address')
    list_filter = ('opening_time', 'closing_time')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'start_time', 'end_time', 'is_available')
    list_filter = ('is_available', 'restaurant')
    search_fields = ('restaurant__name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'date', 'time', 'number_of_guests', 'status')
    list_filter = ('status', 'date', 'restaurant')
    search_fields = ('user__username', 'restaurant__name')
    actions = ['approve_bookings', 'reject_bookings']

    def approve_bookings(self, request, queryset):
        queryset.update(status='confirmed')
    approve_bookings.short_description = "Approve selected bookings"

    def reject_bookings(self, request, queryset):
        queryset.update(status='cancelled')
    reject_bookings.short_description = "Reject selected bookings"

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    list_filter = ('restaurant',)
    search_fields = ('name', 'restaurant__name')

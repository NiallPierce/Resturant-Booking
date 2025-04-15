from django.contrib import admin
from .models import Restaurant, TimeSlot, Booking, MenuItem, Table


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'address', 'opening_time', 'closing_time', 'capacity',
        'contact_number'
    )
    search_fields = ('name', 'address')
    list_filter = ('opening_time', 'closing_time')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'table_number', 'capacity', 'is_active')
    list_filter = ('is_active', 'restaurant')
    search_fields = ('restaurant__name',)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'start_time', 'end_time', 'is_available')
    list_filter = ('is_available', 'restaurant')
    search_fields = ('restaurant__name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'restaurant', 'date', 'time', 'number_of_guests',
        'status', 'created_at'
    )
    list_filter = ('status', 'date', 'restaurant')
    search_fields = ('user__username', 'restaurant__name')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_bookings', 'reject_bookings']
    list_per_page = 20
    date_hierarchy = 'date'
    ordering = ('-date', '-time')

    fieldsets = (
        ('Booking Information', {
            'fields': (
                'user', 'restaurant', 'table', 'time_slot', 'date',
                'time', 'number_of_guests'
            )
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

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

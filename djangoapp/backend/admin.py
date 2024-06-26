from django.contrib import admin
from .models import ServiceOrder

# Register your models here.


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ('service_order_code', 'subject', 'creation_datetime',
                    'user', 'customer', 'priority', 'whatsapp_sent')
    list_filter = ('user', 'customer', 'priority', 'whatsapp_sent')
    search_fields = ('service_order_code', 'subject', 'description')

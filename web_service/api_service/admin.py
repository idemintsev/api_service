from django.contrib import admin
from api_service.models import Customer, Deal


class DealsInLine(admin.TabularInline):
    model = Deal


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'spent_money']
    list_filter = ['name', 'spent_money']
    inlines = [DealsInLine]
    list_display_links = ['name', ]


class DealAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'quantity', 'total', 'date', 'customer', 'transaction_number']
    list_filter = ['item', 'date', 'total', 'quantity', 'customer', 'transaction_number']
    list_display_links = ['item', ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Deal, DealAdmin)

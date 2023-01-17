from django.contrib import admin

from flower_shop_app.models import Flower, FlowerBouquet, FlowerBouquetItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'phone_number', 'client_name', 'created', 'delivery_time']
    list_filter = ['status', 'created', 'delivery_time']
    search_fields = ['phone_number', 'client_name']
    inlines = [
        OrderItemInline,
    ]


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'availability']
    list_filter = ['availability']
    search_fields = ['name']


class FlowerInline(admin.TabularInline):
    model = FlowerBouquetItem
    extra = 1


@admin.register(FlowerBouquet)
class FlowerBouquetAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'availability']
    list_filter = ['availability']
    search_fields = ['name']
    ordering = ['name']
    inlines = [
        FlowerInline,
    ]

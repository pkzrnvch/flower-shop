from django.contrib import admin
from django.utils.safestring import mark_safe

from flower_shop_app.models import (ConsultationRequest,
                                    EventTag,
                                    Flower,
                                    FlowerBouquet,
                                    FlowerBouquetAttribute,
                                    FlowerBouquetAttributeItem,
                                    FlowerBouquetItem,
                                    Order,
                                    OrderItem,
                                    ColorTheme)


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ['status', 'created', 'name', 'phone_number']
    list_filter = ['status', 'created']
    search_fields = ['phone_number']


@admin.register(EventTag)
class EventTagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ColorTheme)
class ColorThemeAdmin(admin.ModelAdmin):
    list_display = ['name']


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


@admin.register(FlowerBouquetAttribute)
class FlowerBouquetAttributeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'availability']
    list_filter = ['availability']
    search_fields = ['name']


class BouquetAttributeInline(admin.TabularInline):
    model = FlowerBouquetAttributeItem
    extra = 1


class FlowerInline(admin.TabularInline):
    model = FlowerBouquetItem
    extra = 1


@admin.register(FlowerBouquet)
class FlowerBouquetAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'availability', 'event_tags_display']
    list_filter = ['availability']
    list_editable = ['availability', 'price']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['bouquet_image']
    inlines = [
        FlowerInline,
        BouquetAttributeInline,
    ]

    def event_tags_display(self, obj):
        return ', '.join(
            [event_tag.name for event_tag in obj.event_tags.all()]
        )
    event_tags_display.short_description = '???????? ??????????????'

    def bouquet_image(self, obj):
        return mark_safe('<img src="{url}" width="300px" />'.format(url=obj.image.url))

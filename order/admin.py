from django.contrib import admin

from order.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "created_at", "update_at", "is_paid", "user", "status_order"
    )
    list_filter = (
        "created_at", "update_at", "is_paid", "status_order"
    )
    search_fields = ("first_name", "address")
    inlines = [OrderItemInline]


admin.site.register(OrderItem)

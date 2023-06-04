from django.contrib import admin
from django.utils.safestring import mark_safe

from product.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "image_show",
        "price",
        "is_available",
        "inventory",
        "created_at",
        "updated_at"
    )
    list_filter = ("is_available", "created_at", "updated_at")
    list_editable = ("price", "is_available")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    def image_show(self, obj):
        if obj.image:
            return mark_safe(
                "<img src='{}' width='60' />".format(obj.image.url)
            )
        return "None"

    image_show.__name__ = "Picture"

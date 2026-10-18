from django.contrib import admin
from .models import Order, OrderItem, ShippingMethod, DiscountCode, DiscountCodeUsage
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_paid",
        "status",
        "shippingmethod",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
        "is_paid",
        "status",
    )
    readonly_fields = (
        "updated_at",
        "created_at",
        "payment_ref_id",
        "delivery_note",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "is_active",
        "user__email",
        "discount_code__code",
        "shippingmethod__name",
    )
    list_editable = (
        "is_active",
    )
    

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "price",
        "discount",
        "quantity",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
    )
    readonly_fields = (
        "updated_at",
        "created_at",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "is_active",
        "product_name",
        "price",
        "quantity",
    )
    list_editable = (
        "is_active",
    )
    

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
    )
    readonly_fields = (
        "updated_at",
        "created_at",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "is_active",
        "name",
        "price",
    )
    list_editable = (
        "is_active",
        "price",
        "name",
    )
    

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "value",
        "max_usage",
        "used_count",
        "expires_at",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
    )
    readonly_fields = (
        "updated_at",
        "created_at",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "is_active",
        "code",
        "max_usage",
        "used_count",
    )
    list_editable = (
        "is_active",
    )
    
    
@admin.register(DiscountCodeUsage)
class DiscountCodeUsageAdmin(admin.ModelAdmin):
    list_display = (
        "code__code",
        "user__email",
        "order__id",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
    )
    readonly_fields = (
        "updated_at",
        "created_at",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "is_active",
    )
    list_editable = (
        "is_active",
    )
    
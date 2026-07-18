from django.contrib import admin
from .models import Category, Brand



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url_name",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
    )
    list_editable = ("is_active",)
    readonly_fields = (
        "updated_at",
        "created_at",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "name",
        "url_name",
    )
    

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url_name",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
    )
    list_editable = ("is_active",)
    readonly_fields = (
        "updated_at",
        "created_at",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "name",
        "url_name",
    )
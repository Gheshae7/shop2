from django.contrib import admin
from .models import ContactUs


# Register your models here.


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "subject",
        "is_active",
        "is_read_by_admin",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
    )
    readonly_fields = (
        "updated_at",
        "created_at",
        "subject",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "is_active",
        "full_name",
        "subject",
        "email",
        "message",
    )
    list_editable = (
        "is_active",
        "is_read_by_admin",
    )
    
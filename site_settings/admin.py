from django.contrib import admin
from .models import FooterBox, FooterLink, SiteSettings, QuestionAnswer, Feature, Ticker
# Register your models here.


class FooterLinkInlineStackedInline(admin.StackedInline):
    model = FooterLink
    extra = 1


@admin.register(FooterBox)
class FooterBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active",)
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("name", "is_active",)
    inlines = (FooterLinkInlineStackedInline,)
    
    
@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "footer_box__name", "url", "is_active", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active",)
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("name", "is_active", "footer_box__name")
    
    
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active",)
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("name", "is_active",)
    
    
@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_active",
        "emoji",
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
    )
    date_hierarchy = "created_at"
    search_fields = (
        "question",
        "answer",
        "emoji",
    )


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "emoji",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
        "emoji",
    )
    readonly_fields = (
        "updated_at",
        "created_at",
    )
    date_hierarchy = "created_at"
    list_editable = ("emoji",)
    search_fields = (
        "title",
        "description",
        "emojy",
    )
  
  
@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_active",
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
    )
    date_hierarchy = "created_at"
    search_fields = (
        "title",
    )
     
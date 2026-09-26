from django.contrib import admin
from .models import BlogCategory, BlogTag, Blog, BlogSection, BlogView, BlogLike, BlogComment, BlogCommentReaction
from django_summernote.admin import SummernoteModelAdmin
from django import forms
from django_summernote.widgets import SummernoteWidget


class BlogSectionForm(forms.ModelForm):
    class Meta:
        model = BlogSection
        fields = "__all__"
        widgets = {
            "content": SummernoteWidget(),
        }
        

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
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


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
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
    )
    
    
@admin.register(BlogSection)
class BlogSectionAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    
    list_display = (
        "blog__name",
        "order",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
        "order",
    )
    list_editable = ("is_active", "order")
    readonly_fields = (
        "updated_at",
        "created_at",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "blog__name",
        "title",
        "content",
    )
 

class BlogSectionStackedInline(admin.StackedInline):
    model = BlogSection
    extra = 1
    form = BlogSectionForm
    summernote_fields = ('content',)

    
@admin.register(Blog)   
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "reading_time",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
        "reading_time",
    )
    list_editable = ("is_active",)
    readonly_fields = (
        "updated_at",
        "created_at",
        "slug",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "name",
        "category",
        "tags",
        "short_text",
        "summary",
    )
    
    inlines = (BlogSectionStackedInline,)


@admin.register(BlogView)
class BlogViewAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "blog__name",
        "ip",
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
        "is_active",
        "ip",
    )
    list_editable = ("is_active",)
    

@admin.register(BlogLike)
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "blog__name",
        "user__email",
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
        "is_active",
        "user__email",
    )
    list_editable = ("is_active",)
    
    
@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "blog__name", "is_active", "name", "author", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active",)
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("name", "blog__name", "title",)
    

@admin.register(BlogCommentReaction)
class BlogCommentReactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "comment",
        "reaction",
        "is_active",
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
        "reaction",
        "comment",
    )
    list_editable = (
        "is_active",
        "reaction",
    )
from django.contrib import admin
from .models import Category, Brand, Product, ProductSpecification, Attribute, AttributeValue, ProductVariant, ProductsImages, Tag, SpecificationCategory, ProductDeliveryInfo, Comment, Banner, ProductView, CommentReaction
from django_summernote.admin import SummernoteModelAdmin



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url_name",
        "emoji",
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
   
   
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
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
    
    
@admin.register(SpecificationCategory)
class SpecificationCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "order",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "is_active",
    )
    list_editable = ("is_active", "order",)
    readonly_fields = (
        "updated_at",
        "created_at",
    )
    date_hierarchy = "created_at"
    search_fields = (
        "name",
        "order",
    )
    

@admin.register(ProductDeliveryInfo)
class ProductDeliveryInfoAdmin(admin.ModelAdmin):
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
   
   
class AttributeValueStackedInline(admin.StackedInline):
    model = AttributeValue
    extra = 1
    
    
class ProductsImagesStackedInline(admin.StackedInline):
    model = ProductsImages
    extra = 1
    
  
class ProductSpecificationStackedInline(admin.StackedInline):
    model = ProductSpecification
    extra = 1  
    
    
class ProductVariantStackedInline(admin.StackedInline):
    model = ProductVariant
    extra = 1
 

@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ("name", "is_active", "category", "brand", "slug", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active", "brand", "category")
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("name", "is_active", "category", "brand", "slug")
    inlines = (ProductSpecificationStackedInline ,ProductVariantStackedInline ,ProductsImagesStackedInline,)
    

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ("name", "product__name", "is_active", "value", "order", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active",)
    list_editable = ("is_active", "value", "order")
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("name", "is_active", "value", "product__name",)
    
    
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active",)
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("name", "is_active", "name",)
    inlines = (AttributeValueStackedInline,)
    

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("pk", "attribute__name", "value", "color_code", "is_active", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active", "attribute__name",)
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("value", "is_active", "attribute__name",)
    
    
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("pk", "product__name", "price", "stock", "discount", "sales_count", "is_active", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active", "product__name", "stock", "price", "sales_count")
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at", "sales_count")
    date_hierarchy = "created_at"
    search_fields = ("is_active", "product__name",)
    
    
@admin.register(ProductsImages)
class ProductsImagesAdmin(admin.ModelAdmin):
    list_display = ("pk", "product__name", "variant__id", "is_main",  "is_active", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_main", "is_active")
    list_editable = ("is_active", "is_main")
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("is_active", "product__name", "is_main")
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "product__name", "is_active", "name", "author", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active",)
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at",)
    date_hierarchy = "created_at"
    search_fields = ("name", "product__name", "title",)
    
    
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "short_title",
        "emoji",
        "id",
        "is_active",
        "btn_text",
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
        "btn_text",
        "short_title",
        "main_title",
    )
    list_editable = (
        "is_active",
        "emoji",
    )
    
    
@admin.register(ProductView)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "product__name",
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
        "product__name",
    )
    list_editable = ("is_active",)
    

@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
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
    
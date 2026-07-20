from django.contrib import admin
from .models import Category, Brand, Product, ProductSpecification, Attribute, AttributeValue, ProductVariant, ProductsImages



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
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "category", "brand", "slug", "updated_at", "created_at",)
    list_filter = ("created_at", "updated_at", "is_active", "brand", "category")
    list_editable = ("is_active",)
    readonly_fields = ("updated_at", "created_at", "count_view")
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
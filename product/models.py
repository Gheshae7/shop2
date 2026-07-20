from django.db import models
from basic.base_model import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator



class Category(BaseModel):
    """This class is for products categories."""
    
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام دسته بندی', unique=True)
    url_name = models.SlugField(max_length=120, null=False, blank=False, verbose_name='آدرس دسته بندی در url', unique=True)
    parent = models.ForeignKey(to='Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته بندی والد', related_name='children_categories')
    image = models.ImageField(upload_to='category/image', null=True, blank=True, verbose_name='عکس دسته بندی', help_text='فقط برای دسته بندی های والد استفاده می شود')
    
    
    def __str__(self):
        parent = '/ والد' if self.parent is None else ''
        return f'{self.name} / {self.url_name} {parent}'
    
    
    class Meta: 
        db_table = 'categories'
        db_table_comment = 'This table for products` categories'
        ordering = ['is_active', 'name', 'url_name',]
        

class Brand(BaseModel):
    """This class is for products brands."""
    
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام برند', unique=True)
    url_name = models.SlugField(max_length=120, null=False, blank=False, verbose_name='آدرس برند در url', unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'brands'
        db_table_comment = 'This table for products` brands'
        ordering = ['is_active', 'name', 'url_name',]


class Product(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام محصول')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته بندی محصول', related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='برند محصول', related_name='products')
    short_description = models.CharField(max_length=255, null=True, blank=True, verbose_name='توضیحات کوتاه محصول')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات اصلی محصول')
    slug = models.SlugField(null=False, blank=False, unique=True, verbose_name='آدرس محصول در url')
    count_view = models.PositiveIntegerField(default=0, verbose_name='بازدید از محصول')
    
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        db_table = 'products'
        db_table_comment = 'This table is for defining products.'
        ordering = ['is_active', 'name', 'category',]
        
            
class ProductSpecification(BaseModel):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام ویژگی')
    value = models.CharField(max_length=255, null=False, blank=False, verbose_name='مقدار ویژگی')
    order = models.PositiveIntegerField(default=0, blank=False, verbose_name='ترتیب نمایش')


    def __str__(self):
        return f'{self.name} / {self.product.name}'


    class Meta:
        db_table = 'product_specifications'
        db_table_comment = 'This table is for product technical specifications and is related to the products table.'
        ordering = ['is_active', 'order']
           

class Attribute(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name='رنگ / حافطه داخلی و ...')


    def __str__(self):
        return self.name
    
    
    class Meta:
        db_table = 'attribute'
        db_table_comment = ''
        ordering = ['is_active', 'name']


class AttributeValue(BaseModel):
    attribute = models.ForeignKey(Attribute, related_name='values_attr', on_delete=models.CASCADE, verbose_name='ویژگی')
    value = models.CharField(max_length=155, null=True, blank=True, verbose_name='مقدار ویژگی')
    color_code = models.CharField(max_length=7, blank=True, null=True, verbose_name='کد رنگ', help_text='اگر از ویژگی رنگ استفاده کردی کد رنگ رو اینجا بزار')

    def __str__(self):
        return f"{self.attribute.name} / {self.value}"
    
    
    class Meta:
        db_table = 'attribute_values'
        db_table_comment = ''
        unique_together = ('attribute', 'value')
        ordering = ['is_active', 'value']
        
    
class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, related_name='variants', verbose_name='محصول والد')
    attributes = models.ManyToManyField(AttributeValue, related_name='variants')
    price = models.PositiveIntegerField(null=False, blank=False, verbose_name='قیمت محصول')
    stock = models.PositiveIntegerField(default=0,blank=True, verbose_name='موجودی محصول')
    discount = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name='درصد تخفیف', null=True, blank=True, help_text='اگر می خواهید برای این محصول تخفیف بزارید این فیلد باید پر شود')
    sales_count = models.PositiveIntegerField(default=0, verbose_name="تعداد به فروش رفته")
    
    
    def __str__(self):
        return f'{self.product.name} / {self.pk}'
    
    
    class Meta:
        db_table = 'product_variant'
        db_table_comment = ''
        ordering = ['is_active', 'stock',]
    
     
class ProductsImages(BaseModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, related_name='images', on_delete=models.CASCADE, null=True, blank=True, help_text='اگر این عکس مخصوص محصول خاصی است مثل رنگ قرمز')
    image = models.ImageField(upload_to='product/image', verbose_name='عکس محصول', null=False, blank=False)
    is_main = models.BooleanField(default=False, verbose_name='عکس اصلی / غیر اصلی')

    class Meta:
        db_table = 'products_images'
        db_table_comment = ''
        ordering = ['is_active']
        

    def __str__(self):
        return f"Image for {self.product.name}"

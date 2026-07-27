from django.db import models
from basic.base_model import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import User



class Category(BaseModel):
    """This class is for products categories."""
    
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام دسته بندی', unique=True)
    url_name = models.SlugField(max_length=120, null=False, blank=False, verbose_name='آدرس دسته بندی در url', unique=True)
    parent = models.ForeignKey(to='Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته بندی والد', related_name='children_categories')
    image = models.ImageField(upload_to='category/image', null=True, blank=True, verbose_name='عکس دسته بندی', help_text='فقط برای دسته بندی های والد استفاده می شود')
    emoji = models.CharField(max_length=10, null=False, blank=False, default='🟦', verbose_name='ایموجی این دسته بندی')
    
    
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


class Tag(BaseModel):
    name = models.CharField(max_length=100, unique=True, blank=False, name=False, verbose_name='نام تگ')
    
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        db_table = 'tags'
        db_table_comment = 'This is for tag`s products'
        ordering = ['name']


class ProductDeliveryInfo(BaseModel):
    title = models.CharField(max_length=55, null=False, blank=False, verbose_name='عنوان')
    description = models.CharField(max_length=255, null=False, blank=False, verbose_name='توضیحات')
    emoji = models.CharField(max_length=10, null=False, blank=True, verbose_name='اموجی', help_text='برای قشنگی بزاریش خیلی بهتر عمویی')
    
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        db_table = 'product_delivery_info'
        db_table_comment = 'f'
        ordering = ['is_active',]
    

class Product(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='نام محصول')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته بندی محصول', related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='برند محصول', related_name='products')
    tag = models.ManyToManyField(Tag, null=True, blank=True, verbose_name='تگ های محصول')
    delivery_info = models.ManyToManyField(ProductDeliveryInfo, verbose_name='اطلاعاتی مانند نوع بسته بندی و این حرفا',)
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
        
        
class SpecificationCategory(BaseModel):
    name = models.CharField(max_length=155, null=False, blank=False, verbose_name='نام دسته بندی ویژگی')
    order = models.PositiveIntegerField(default=0, blank=False, verbose_name='ترتیب نمایش')

    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'specificationcategory'
        db_table_comment = 'd'
        ordering = ['order']
        
            
class ProductSpecification(BaseModel):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    category = models.ForeignKey(SpecificationCategory ,on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته بندی ویژگی', related_name='product_specification')
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام ویژگی')
    value = models.CharField(max_length=255, null=False, blank=False, verbose_name='مقدار ویژگی')
    short_description = models.CharField(max_length=255, null=True, blank=True, verbose_name='توضیحی در مورد ویژگی', help_text='اگر تیک ویژگی کلیدی را زده اید توضیح ویژگی را اینجا بگذارید')
    order = models.PositiveIntegerField(default=0, blank=False, verbose_name='ترتیب نمایش')
    is_key_feature = models.BooleanField(default=False, verbose_name='ویژگی کلیدی')
    is_quick_info = models.BooleanField(default=False, verbose_name='اطلاعات سریع')


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


class ProductQuestionAnswer(BaseModel):
    question = models.TextField(verbose_name='پرسش')
    answer = models.TextField(verbose_name='پاسخ')
    
    def __str__(self):
        return self.question
    
    
    class Meta:
        db_table = 'product_question_answers'
        db_table_comment = 'd'
        ordering = ['is_active']
        
        
class Comment(BaseModel):
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE, verbose_name='محصول', related_name='comments')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='عنوان کامنت')
    text = models.TextField(max_length=255, null=False, blank=False, verbose_name='متن کامنت')
    rating = models.SmallIntegerField(validators=(MaxValueValidator(5), MinValueValidator(0)), verbose_name='امتیاز',)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر', help_text='اگر کاربری که در سایت ثبت نام کرده باشد و این کامنت را بگذارد این مقدار پر می شود')
    name = models.CharField(max_length=100, null=True, blank=True, default='ناشناس', verbose_name='نام نویسنده', help_text='اگر کسی در سایت ما ثبت نام نکرده باشد و سپس کامنت بزاره ما اسمش رو از اینحا میزاریم اگر اسم پر نکنه به عنوان ناشناس این رو نشون میدیم')
    like = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='لایک')
    dislike = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='دیسلایک')
    
    
    def __str__(self):
        return f'{self.pk} / {self.product}'
    
    
    class Meta:
        db_table = 'comments_products'
        db_table_comment = 'c'
        ordering = ['is_active', '-created_at']
    
from django.db import models
from basic.base_model import BaseModel
from account.models import User
from django.utils.translation import gettext_lazy as _
from product.models import ProductVariant
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class DiscountCode(BaseModel):
    """This class is for discount codes."""

    code = models.CharField(max_length=50, unique=True, verbose_name='کد تخفیف')
    value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name='درصد تخفیف')
    max_usage = models.PositiveIntegerField(null=True, blank=True, verbose_name='حداکثر تعداد استفاده', help_text='خالی بگذارید تا نامحدود باشد')
    used_count = models.PositiveIntegerField(default=0, verbose_name='تعداد استفاده شده')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ انقضا')

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'discount_codes'
        db_table_comment = 'This table is for discount codes.'
        ordering = ['is_active',]


class DiscountCodeUsage(BaseModel):
    """Which user used which code on which order."""

    code = models.ForeignKey(DiscountCode, on_delete=models.PROTECT, related_name='usages', verbose_name='کد تخفیف')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='discount_usages', verbose_name='کاربر')
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='discount_usage', verbose_name='سفارش')

    def __str__(self):
        return f'{self.code} / {self.user}'

    class Meta:
        db_table = 'discount_code_usages'
        db_table_comment = 'This table records each use of a discount code.'
        ordering = ['is_active',]
        constraints = [
            models.UniqueConstraint(fields=['code', 'user'], name='unique_discount_code_per_user'),
        ]



class ShippingMethod(BaseModel):
    """This class is for the delivery method."""
    
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='نام روش ارسال')
    price = models.PositiveIntegerField(verbose_name='هزینه ارسال')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'shipping_method'
        db_table_comment = 'This table is for the delivery method.'
        ordering = ['is_active',]
        


class Order(BaseModel):
    """This table is for user orders."""
    
    class StatusChoice(models.TextChoices):
        PLACED = 'placed', 'ثبت سفارش'
        PROCESSING = 'processing', 'پردازش انبار'
        SHIPPED = 'shipped', 'تحویل به سفیر'
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر', related_name='orders')
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کد تخفیف استفاده شده')
    amount = models.PositiveBigIntegerField(default=0, verbose_name='جمع پرداختی بدون تخفییف')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده یا نشده')
    delivery_note = models.TextField(null=True, blank=True, verbose_name='توضیحات گیرنده')
    amount_discount = models.PositiveBigIntegerField(default=0, verbose_name='جمع تخفیف ها')
    status = models.CharField(max_length=20 ,choices=StatusChoice, default=StatusChoice.PLACED, null=True, blank=True, verbose_name='وضعیت سفارش')
    receiver_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='نام گیرنده')
    receiver_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='موبایل گیرنده')
    receiver_address = models.TextField(verbose_name='آدرس گیرنده', null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان پرداخت')
    payment_ref_id = models.CharField(max_length=500, null=True, blank=True, verbose_name='کد پیگیری درگاه')
    shippingmethod = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='روش ارسال')
    shipping_cost = models.PositiveIntegerField(default=0, verbose_name='هزینه ارسال', null=True, blank=True)
    
    def __str__(self):
        return f'{self.user} / {self.id}'
    
    class Meta:
        db_table = 'orders'
        db_table_comment = 'This table is for user orders.'
        ordering = ['is_active', '-created_at']


class OrderItem(BaseModel):
    """This class is created for products that are included in an order."""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False,  verbose_name='کدام سفارش', related_name='order_items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, verbose_name='کدام محصول')
    product_name = models.CharField(max_length=255, verbose_name='نام محصول در زمان خرید', null=True, blank=True)
    price = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='قیمت محصول')
    discount = models.PositiveSmallIntegerField(default=0 ,validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='درصد تخفیف', null=True, blank=True,)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='چه تعداد از این محصول', null=True, blank=True,)
    
    def __str__(self):
        return f'{self.order.id} / {self.product_variant.product.name}'
    
    
    class Meta:
        db_table = 'order_items'
        db_table_comment = 'This table is created for products that are included in an order.'
        ordering = ['is_active',]

from django import template
from product.models import Category
from django.db.models import Prefetch, Subquery, OuterRef, Count
from site_settings.models import FooterBox, SiteSettings
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from order.models import OrderItem, Order
from product.models import ProductsImages
from django.db.models.functions import Coalesce

register = template.Library()


# This inclusion_tag is for the site header
@register.inclusion_tag('header_base.html')
def header_base(request):

    if request.user.is_authenticated:
        order = Order.objects.filter(
            is_active=True,
            user=request.user,
            status='placed',
            is_paid=False,
        ).first()
        totals = OrderItem.objects.filter(
            order=order,
            is_active=True,
        ).aggregate(
            items_count=Count('id'),
        )

        return {
            'request': request,
            'categories': Category.objects.filter(
                is_active=True,
                parent__isnull=True,
                children_categories__is_active=True,
            ).prefetch_related(
                Prefetch(
                    'children_categories',
                    queryset=Category.objects.filter(is_active=True)
                )
            ).distinct(),
            'site_setting': SiteSettings.objects.filter(
                is_active=True
            ).values('logo', 'phone', 'address', 'youtube_channel', 'linkedin_channel', 'instagram_channel', 'telegram_channel').first(),
            'MEDIA_URL': settings.MEDIA_URL,
            'total_order_item':  totals['items_count'],
        }
    return {
        'request': request,
        'categories': Category.objects.filter(
            is_active=True,
            parent__isnull=True,
            children_categories__is_active=True,
        ).prefetch_related(
            Prefetch(
                'children_categories',
                queryset=Category.objects.filter(is_active=True)
            )
        ).distinct(),
        'site_setting': SiteSettings.objects.filter(
            is_active=True
        ).values('logo', 'phone', 'address', 'youtube_channel', 'linkedin_channel', 'instagram_channel', 'telegram_channel').first(),
        'MEDIA_URL': settings.MEDIA_URL,
    }


# This inclusion_tag is for the site footer
@register.inclusion_tag('footer_base.html')
def footer_base():
    return {
        'categories': Category.objects.filter(is_active=True, parent__isnull=False,)[:5],
        'footer_boxes': FooterBox.objects.filter(is_active=True,).prefetch_related('footer_links'),
        'site_setting': SiteSettings.objects.filter(is_active=True).first(),
    } 


@register.simple_tag
def calculating_discount(price, discount):
    result = int(price - ((price / 100) * discount))
    saving = price - result
    return (result, saving)


@register.filter
def times(number):
    number = int(number)
    return range(1, number + 1)


@register.simple_tag
def calculateing_darsad_rating(comment_count, comments, number):
    count = 0
    for comment in comments:
        if comment.rating == number:
            count += 1
            
    res = (100 / comment_count) * count if comment_count != 0 else None
    return round(res) if res else None


@register.simple_tag
def get_page_range(current_page, total_pages, window=3):
    pages = []
    end = min(current_page + window, total_pages)
    for p in range(current_page, end + 1):
        pages.append(p)
    if end < total_pages:
        if end < total_pages - 1:
            pages.append('...')
        pages.append(total_pages)
    return pages


@register.simple_tag
def is_new(created_at, hours=1):
    if not created_at:
        return False
    return True if timezone.now() - created_at < timedelta(hours=hours) else False
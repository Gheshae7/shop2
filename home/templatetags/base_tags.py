from django import template
from product.models import Category
from django.db.models import Prefetch

register = template.Library()


@register.inclusion_tag('header_base.html')
def header_base(request):
    categories = Category.objects.filter(is_active=True, parent__isnull=True, children_categories__is_active=True,).prefetch_related(Prefetch('children_categories', queryset=Category.objects.filter(is_active=True))).distinct()
    return {
        'request': request,
        'categories': categories,
    } 



@register.inclusion_tag('footer_base.html')
def footer_base():
    pass 
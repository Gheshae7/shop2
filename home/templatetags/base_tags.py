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
            
    res = (100 / comment_count) * count
    return round(res)
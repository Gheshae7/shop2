from django import template

register = template.Library()


@register.inclusion_tag('header_base.html')
def header_base(request):
    return {
        'request': request,
    } 



@register.inclusion_tag('footer_base.html')
def footer_base():
    pass 
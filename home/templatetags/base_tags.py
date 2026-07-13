from django import template
# from account

register = template.Library()


@register.inclusion_tag('header_base.html')
def header_base(request):
    # user = 
    return {
        'request': request,
    } 



@register.inclusion_tag('footer_base.html')
def footer_base():
    pass 
from django.shortcuts import render
from django.views.generic import TemplateView
from product.models import Category, Product, Brand  
from site_settings.models import QuestionAnswer, Feature, Ticker
from django.db.models import Count

# Create your views here.


class HomePageView(TemplateView):
    """This class displays the main page."""
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True, parent__isnull=False).annotate(stock=Count('products'))
        context['brands'] = Brand.objects.filter(is_active=True,).order_by('?')[:8]
        context['products_count'] = Product.objects.filter(is_active=True).aggregate(Count('id'))['id__count']
        context['questions'] = QuestionAnswer.objects.filter(is_active=True).order_by('?')[:6]
        context['features'] = Feature.objects.filter(is_active=True).order_by('?')[:4]
        context['tickers'] = Ticker.objects.filter(is_active=True).order_by('?')[:6]
        return context
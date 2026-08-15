from django.shortcuts import render
from django.views.generic import TemplateView
from product.models import Category, Product, Brand, ProductsImages
from site_settings.models import QuestionAnswer, Feature, Ticker, HeroSection
from django.db.models import Count, Prefetch, Sum, Min, Max, Avg
from django.utils.timezone import now
from datetime import timedelta

# Create your views here.


class HomePageView(TemplateView):
    """This class displays the main page."""
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True, parent__isnull=False).annotate(stock=Count('products')).order_by('-stock')
        context['brands'] = Brand.objects.filter(is_active=True,).order_by('?')[:8]
        context['products_count'] = Product.objects.filter(is_active=True).aggregate(Count('id'))['id__count']
        context['questions'] = QuestionAnswer.objects.filter(is_active=True, position__exact='home').order_by('?')[:6]
        context['features'] = Feature.objects.filter(is_active=True).order_by('?')[:4]
        context['tickers'] = Ticker.objects.filter(is_active=True).order_by('?')[:6]
        context['hero_section'] = HeroSection.objects.filter(is_active=True).first()
        context['show_sort_by'] = self.request.GET.get('order_by')
        products_query = Product.objects.filter(is_active=True,).prefetch_related(Prefetch('images', queryset=ProductsImages.objects.filter(is_active=True, is_main=True))).select_related('category', 'brand').annotate(discount=Max('variants__discount'), price=Min('variants__price'), sales_count=(Sum('variants__sales_count')), rating=Avg('comments__rating'), stock=Sum('variants__stock'), comment_count=Count('comments__id', distinct=True), count_view=Count('count_views', distinct=True))
        context['seven_days_ago'] = now() - timedelta(days=7)
        
        # order
        order_by_params = self.request.GET.get('order_by')
        
        
        # region order by
        
        # sort by popular_params
        if order_by_params == 'popular':
            products_query = products_query.order_by('-count_view', '-sales_count')
            
        
        # sort by price_asc_params
        if order_by_params == 'price_asc':
            products_query = products_query.order_by('price')
            
        
        # sort by price_desc_params
        if order_by_params == 'price_desc':
            products_query = products_query.order_by('-price')

        
        # sort by rating_params
        if order_by_params == 'rating':
            products_query = products_query.order_by('-rating')
            
            
        # sort by newest
        if order_by_params == 'newest':
            products_query = products_query.order_by('-created_at')
            
        # endregion sort by
        
        context['products'] = products_query
        
        # order
        order_by_params = self.request.GET.get('order_by')
        
        return context
        
        
    def get_template_names(self):

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['home/includes/grid_view_products.html']

        return [self.template_name]
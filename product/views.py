from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product, ProductsImages, Category, ProductVariant, AttributeValue, Tag, SpecificationCategory, ProductSpecification, ProductDeliveryInfo, Comment, Banner
from site_settings.models import Feature
from site_settings.models import QuestionAnswer
from django.db.models import Prefetch, Max, Min, Sum, Count, Avg, Subquery, OuterRef, Q
from django.utils.timezone import now, timedelta


class ProductListView(ListView):
    """This class is designed to display products to the user and includes filtering capabilities based
on category and other criteria.
"""
    
    template_name = 'product/products.html'
    model = Product
    context_object_name = 'products'
    
    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True,).prefetch_related(Prefetch('images', queryset=ProductsImages.objects.filter(is_active=True, is_main=True))).select_related('category').annotate(discount=Max('variants__discount'), price=Min('variants__price'), sales_count=(Sum('variants__sales_count')), rating=Avg('comments__rating'), stock=Sum('variants__stock'))

        # get category_params
        category_params = self.request.GET.get('category')
        popular_params = self.request.GET.get('popular')
        price_asc_params = self.request.GET.get('price-asc')
        price_desc_params = self.request.GET.get('price-desc')
        rating_params = self.request.GET.get('rating')
        newest_params = self.request.GET.get('newest')
        min_price = self.request.GET.get('min-price')
        max_price = self.request.GET.get('max-price')
        discount_params = self.request.GET.get('discount')
        stock_params = self.request.GET.get('stock')
        
        # fiter by category_params
        if category_params:
            query = query.filter(category__url_name__exact=category_params)
            
        
        # filter by popular_params
        if popular_params == 'true':
            query = query.order_by('-count_view', '-sales_count')
            
        
        # filter by price_asc_params
        if price_asc_params == 'true':
            query = query.order_by('price')
            
        
        # filter by price_desc_params
        if price_desc_params == 'true':
            query = query.order_by('-price')
            
        
        # filter by rating_params
        if rating_params == 'true':
            query = query.order_by('-rating')
        
        
        # filter by newest_params
        if newest_params == 'true':
            query = query.order_by('-created_at')
            
        
        # filter by min_price
        if min_price:
            query = query.filter(price__gte=min_price)
            
            
        # filter by max_price
        if max_price:
            query = query.filter(price__lte=max_price)


        # filter by discount_params
        if discount_params == 'true':
            query = query.filter(discount__isnull=False)
            
            
         # filter by stock_params
        if stock_params == 'true':
            query = query.filter(stock__gte=1)
            

        return query
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seven_days_ago'] = now() - timedelta(days=7)
        context['categories'] = Category.objects.filter(is_active=True).order_by('?')[:9]
        context['max_price'] = ProductVariant.objects.aggregate(Max('price'))['price__max']
        context['min_price'] = ProductVariant.objects.aggregate(Min('price'))['price__min']
        context['banner'] = Banner.objects.filter(is_active=True,).first()
        context['features'] = Feature.objects.filter(is_active=True, position__exact='products').order_by('?')[:4]
        return context
    
    

class ProductDetailView(DetailView):
    """This class is intended to display the details of a product."""
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset(*args, **kwargs)
        query = query.select_related('category', 'brand').prefetch_related(Prefetch('images', queryset=ProductsImages.objects.filter(is_active=True)), Prefetch('comments', queryset=Comment.objects.filter(is_active=True,))).annotate(stock=Sum('variants__stock'), sales_count=Sum('variants__sales_count'), discount=Max('variants__discount'), price=Min('variants__price'), comments_avg=Avg('comments__rating'))
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seven_days_ago'] = now() - timedelta(days=7)
        context['attributes'] = AttributeValue.objects.filter(variants__product=self.object, is_active=True).select_related('attribute').distinct()
        context['images_json'] = [
            {'url': img.image.url, 'is_main': img.is_main}
            for img in self.object.images.all()
        ] or [{'url': '/static/images/no-image.png', 'is_main': True}]
        context['tags'] = Tag.objects.filter(is_active=True, product=self.object)
        context['specifications_categories'] = SpecificationCategory.objects.filter(is_active=True, product_specification__product=self.object).prefetch_related(Prefetch('product_specification', queryset=ProductSpecification.objects.filter(is_active=True))).distinct()
        context['question_answer'] = QuestionAnswer.objects.filter(Q(position__exact='product_detail')|Q(product=self.object), is_active=True,)
        context['deliveries_info'] = ProductDeliveryInfo.objects.filter(is_active=True, product=self.object)
        context['comments_count'] = self.object.comments.aggregate(Count('id'))['id__count']
        first_image = ProductsImages.objects.filter(product=OuterRef('pk'), is_main=True, is_active=True).values_list('image',)[:1]
        context['popular_poducts'] = Product.objects.filter(is_active=True).select_related('category', 'brand').annotate(discount=Max('variants__discount'), sales_count=Sum('variants__sales_count', distinct=True), price=Min('variants__price')).order_by('-count_view', '-sales_count').prefetch_related(Prefetch('images', queryset=ProductsImages.objects.filter(is_active=True, is_main=True)))[:10]

        return context
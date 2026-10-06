from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Blog, BlogCategory, BlogTag, BlogSection, BlogComment, BlogCommentReaction, BlogView, BlogLike
from django.db.models import Count, Prefetch, Q, Exists, OuterRef, BooleanField, Value, Avg, Min, Max
from product.models import Product, ProductsImages


class BlogsListView(ListView):
    model = Blog
    context_object_name = 'blogs'
    template_name = 'blog/blogs.html'
    paginate_by = 1
    
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset()
        query = query.filter(is_active=True,).annotate(count_like=Count('count_likes', distinct=True),
            count_comment=Count('blog_comments', distinct=True),).select_related('category').order_by('-created_at')
        
        category_url_name = self.kwargs.get('url_name')
        if category_url_name:
            query = query.filter(category__url_name=category_url_name)
        
        # order
        order_by_params = self.request.GET.get('order_by')

    # region order by
     
        # sort by oldest
        if order_by_params == 'قدیمی‌ترین ها':
            query = query.order_by('created_at')
            
            
        # sort by newest
        if order_by_params == 'جدیدترین ها':
            query = query.order_by('-created_at')
            
            
        # sort by popular
        if order_by_params == 'محبوب‌ترین ها':
            query = query.order_by('-count_like')
            
    # endregion sort by
        
        return query
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.filter(is_active=True).annotate(count_blog=Count('blogs_c')).order_by('-count_blog')
        return context
    
    
    def get_template_names(self):

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['blog/includes/blogs_list.html']

        return [self.template_name]
    
    
def get_client_ip(request, blog_detail_ip):
    ip_address = request.META.get('REMOTE_ADDR')
    blog_view, created = BlogView.objects.get_or_create(ip=ip_address, blog_id=blog_detail_ip)
    if created:
        print('created new blog_view')
    else:
        print('not created new blog_view')   
    
    
class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog/blog_detail.html'
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset()
        
        if self.request.user.is_authenticated:
            user_blog_like_subquery = BlogLike.objects.filter(is_active=True, blog_id=OuterRef('pk'), user_id=self.request.user.id)
            query = query.annotate(is_liked_by_user=Exists(user_blog_like_subquery))
        else:
            query = query.annotate(is_liked_by_user=Value(False, output_field=BooleanField()))
        
        query = query.filter(is_active=True).select_related('category').annotate(
            count_like=Count('count_likes', distinct=True),
            count_comment=Count('blog_comments', distinct=True),
            count_view=Count('count_views', distinct=True),
            ).prefetch_related(Prefetch('blog_sections', queryset=BlogSection.objects.filter(is_active=True)),
                Prefetch('blog_comments', queryset=BlogComment.objects.filter(is_active=True, parent__isnull=True).prefetch_related(Prefetch('child_comment', queryset=BlogComment.objects.filter(is_active=True, parent__isnull=False).select_related('author'))).annotate(count_like_reaction=Count('blog_reactions', filter=Q(blog_reactions__reaction='like'))).select_related('author').order_by('-created_at')), Prefetch('product', queryset=Product.objects.filter(is_active=True).annotate(rating=Avg('comments__rating'), count_view=Count('count_views', distinct=True), price=Min('variants__price')).order_by('?').prefetch_related(Prefetch('images', queryset=ProductsImages.objects.filter(is_active=True, is_main=True))))
            )
        return query
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = BlogTag.objects.filter(is_active=True, blog=self.object)
        context['popular_tags'] = BlogTag.objects.filter(is_active=True).annotate(count_blog=Count('blog')).order_by('-count_blog')
        context['next_previous_blog'] = Blog.objects.filter(Q(pk=(self.object.id - 1)) | Q(pk=(self.object.id + 1)) ,is_active=True).values('name', 'slug', 'id').order_by('id')
        context['related_blogs'] = Blog.objects.filter(Q(category=self.object.category) | Q(tag__in=self.object.tag.all()) ,is_active=True).order_by('-created_at')[:3]
        context['special_product'] = Product.objects.filter(is_active=True, variants__discount__isnull=False).annotate(discount=Max('variants__discount'), rating=Avg('comments__rating'), count_view=Count('count_views', distinct=True), price=Min('variants__price')).order_by('?').prefetch_related(Prefetch('images', queryset=ProductsImages.objects.filter(is_active=True, is_main=True))).first()
        get_client_ip(self.request, self.object.id)
        return context
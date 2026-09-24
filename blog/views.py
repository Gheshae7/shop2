from django.shortcuts import render
from django.views.generic import ListView
from .models import Blog, BlogCategory
from django.db.models import Count


class BlogsListView(ListView):
    model = Blog
    context_object_name = 'blogs'
    template_name = 'blog/blogs.html'
    
    
    def get_queryset(self, *args, **kwargs):
        query = super().get_queryset()
        query = query.filter(is_active=True,).annotate(count_like=Count('count_likes')).select_related('category')
        
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
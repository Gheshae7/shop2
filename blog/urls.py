from django.urls import path
from .views import BlogsListView, BlogDetailView, add_comment_blog, add_comment_blog_react, like_comment

app_name = 'blog'


urlpatterns = [
    path('', BlogsListView.as_view(), name='blogs_page'),
    path('detail/add_comment_blog', add_comment_blog, name='add_comment_blog'),
    path('detail/add_comment_blog_react', add_comment_blog_react, name='add_comment_blog_react'),
    path('detail/like', like_comment, name='like_comment'),
    path('category/<url_name>', BlogsListView.as_view(), name='blogs_by_category_page'),
    path('detail/<str:slug>', BlogDetailView.as_view(), name='blog_detail_page'),
]

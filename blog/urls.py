from django.urls import path
from .views import BlogsListView

app_name = 'blog'


urlpatterns = [
    path('', BlogsListView.as_view(), name='blogs_page'),
    path('category/<url_name>', BlogsListView.as_view(), name='blogs_by_category_page')
]

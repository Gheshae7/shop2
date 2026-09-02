from django.urls import path
from .views import ProductListView, ProductDetailView, get_price, add_comment_product, like_dislike_comments


app_name = 'product'


urlpatterns = [
    path('', ProductListView.as_view(), name='products_page'),
    path('detail/get_price', get_price, name='get_price'),
    path('detail/add_comment_product', add_comment_product, name='add_comment'),
    path('detail/like_dislike', like_dislike_comments, name='like_dislike_comments'),
    path('detail/<slug:slug>', ProductDetailView.as_view(), name='product_detail_page'),
]
from django.urls import path
from .views import ProductListView, ProductDetailView


app_name = 'product'


urlpatterns = [
    path('', ProductListView.as_view(), name='products_page'),
    path('detail/<slug:slug>', ProductDetailView.as_view(), name='product_detail_page'),
]
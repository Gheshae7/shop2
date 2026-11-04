from django.urls import path
from .views import OrderView, AddOrderItem

app_name = 'order'


urlpatterns = [
    path('', OrderView.as_view(), name='order_page'),
    path('add-order-item', AddOrderItem.as_view(), name='add_order_item'),
]

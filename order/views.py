from django.shortcuts import render
from django.views import View
from product.models import ProductVariant, AttributeValue, ProductsImages
from .models import Order, OrderItem
from django.db.models import Prefetch, OuterRef, Subquery
from django.db.models.functions import Coalesce
# Create your views here.


class OrderView(View):
    def get(self, request, **kwargs):
        
        variant_image = ProductsImages.objects.filter(
        is_active=True, variant=OuterRef('product_variant'),
        ).order_by('-is_main', 'id').values('image')[:1]
        
        product_image = ProductsImages.objects.filter(
        is_active=True, product=OuterRef('product_variant__product'), variant__isnull=True,
        ).order_by('-is_main', 'id').values('image')[:1]
        
        order = Order.objects.filter(
            is_active=True,
            user_id=request.user.id,
            status='placed',
            is_paid=False
        ).prefetch_related(
            Prefetch(
                'order_items',
                queryset=OrderItem.objects.filter(
                    is_active=True
                )
                .select_related('product_variant', 'product_variant__product__category',)
                .annotate(image_path=Coalesce(Subquery(variant_image), Subquery(product_image)))
                .prefetch_related(
                    Prefetch(
                        'product_variant__attributes',
                        queryset=AttributeValue.objects.filter(
                            is_active=True
                        ).select_related('attribute')
                    ),
                )
            )
        ).first()
        context = {
            'order': order
        }
        return render(request, 'order/order.html', context)
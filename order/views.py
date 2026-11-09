from django.shortcuts import render
from django.views import View
from product.models import ProductVariant, AttributeValue, ProductsImages, Product
from .models import Order, OrderItem, ShippingMethod
from django.db.models import Prefetch, OuterRef, Subquery, F, Min, Max, Avg, Sum, Count, Q, Exists

from django.db.models.functions import Coalesce
# Create your views here.
from django.http import Http404, JsonResponse
import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.db import transaction


class OrderView(View):

    def get_template(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return 'order/includes/page_content_in_order.html'

        return 'order/order.html'

    def get(self, request, **kwargs):
        context = {}
        if request.user.is_authenticated:
            variant_image = ProductsImages.objects.filter(
                is_active=True,
                variant=OuterRef('product_variant'),
            ).order_by('-is_main', 'id').values('image')[:1]

            product_image = ProductsImages.objects.filter(
                is_active=True,
                product=OuterRef('product_variant__product'),
                variant__isnull=True,
            ).order_by('-is_main', 'id').values('image')[:1]

            order = Order.objects.filter(
                is_active=True,
                user=request.user,
                status='placed',
                is_paid=False
            ).first()

            if order is None:
                return render(
                    request,
                    self.get_template(request),
                    context= {}
                )

            shipping_method_id = request.GET.get('shipping_method')

            if shipping_method_id:
                shipping = get_object_or_404(
                    ShippingMethod,
                    id=shipping_method_id,
                    is_active=True,
                )

                order.shippingmethod = shipping
                order.shipping_cost = shipping.price

                order.save(update_fields=[
                    'shippingmethod',
                    'shipping_cost',
                ])
                
            inc_quantity = request.GET.get('inc_quantity') 
            dec_quantity = request.GET.get('dec_quantity') 
            
            if inc_quantity and inc_quantity == 'true':
                order_item = OrderItem.objects.filter(is_active=True, id=request.GET.get('item_id'), order_id=order.id).select_related('product_variant').first()
                if order_item.quantity + 1 > order_item.product_variant.stock:
                    return JsonResponse({
                        'success': 'false',
                    })
                else:
                    order_item.quantity = F('quantity') + 1
                    order_item.save(update_fields=['quantity'])
                    order_item.refresh_from_db(fields=['quantity'])
                    # return JsonResponse({
                    #     'success': 'true',
                    #     'action': 'inc',
                    #     'message': 'Done',
                    #     'value': order_item.quantity
                    # })
                    
            if dec_quantity and dec_quantity == 'true':
                order_item = OrderItem.objects.filter(is_active=True, id=request.GET.get('item_id'), order_id=order.id).select_related('product_variant').first()
                if order_item.quantity - 1 <= 0:
                    return JsonResponse({
                        'success': 'false',
                    })
                else:
                    order_item.quantity = F('quantity') - 1
                    order_item.save(update_fields=['quantity'])
                    order_item.refresh_from_db(fields=['quantity'])
            
            remove_id = request.GET.get('remove_id')
            if remove_id:
                deleted_count, details = OrderItem.objects.filter(
                    id=remove_id,
                    order_id=request.GET.get('order_id')
                ).delete()
            
            order_items = OrderItem.objects.filter(
                is_active=True
            ).select_related(
                'product_variant',
                'product_variant__product__category',
            ).annotate(
                image_path=Coalesce(
                    Subquery(variant_image),
                    Subquery(product_image),
                ),
            ).prefetch_related(
                Prefetch(
                    'product_variant__attributes',
                    queryset=AttributeValue.objects.filter(
                        is_active=True
                    ).select_related('attribute')
                )
            ).order_by('-quantity')
            
            sort_by = request.GET.get('order_by')
            if sort_by is not None:
                if sort_by == 'price-asc':
                    order_items = order_items.order_by('product_variant__price')
                if sort_by == 'price-desc':
                    order_items = order_items.order_by('-product_variant__price')
                if sort_by == 'name':
                    order_items = order_items.order_by('product_variant__product__name')
                    
            order = Order.objects.filter(
                pk=order.pk
            ).select_related(
                'shippingmethod'
            ).prefetch_related(
                Prefetch(
                    'order_items',
                    queryset=order_items
                )
            ).first()

            shippings = ShippingMethod.objects.filter(is_active=True)
            
            cart_items = OrderItem.objects.filter(
                order__user=self.request.user,
                order__is_active=True,
                order__status='placed',
                order__is_paid=False,
                product_variant__product_id=OuterRef('pk'),
                is_active=True,
            )
            
            related_products = Product.objects.filter(is_active=True).select_related('category').annotate(discount=Max('variants__discount'), count_view=Sum('count_views', distinct=True), price=Min('variants__price'), rating=Avg('comments__rating', distinct=True), is_in_cart=Exists(cart_items)).order_by('-rating').prefetch_related(Prefetch('images', queryset=ProductsImages.objects.filter(is_active=True, is_main=True)))[:6]
        

            total_quantity = OrderItem.objects.filter(
                order=order,
                is_active=True,
            ).aggregate(
                total=Sum('quantity')
            )['total'] or 0

            context = {
                'order': order,
                'shippings': shippings,
                'related_products': related_products,
                'selected_sort_by': sort_by if sort_by else 'default',
                'total_quantity': total_quantity,
            }

            return render(
                request,
                self.get_template(request),
                context
            )
        else:
            return render(
                request,
                self.get_template(request),
                context
            )
        
        
        
def add_order_item(request, data, order: None):
    product_variant = ProductVariant.objects.filter(
    product_id=data.get('product_id'),
            is_active=True,
        ).annotate(
            matched_attributes=Count(
                'attributes',
                filter=Q(
                    attributes__value__in=[
                        data.get('color'),
                        data.get('size'),
                    ],
                    attributes__is_active=True,
                ),
                distinct=True,
            )
        ).filter(
            matched_attributes=2
        ).first()
    if product_variant is not None:
        quantity = data.get('qty')
        if int(quantity) > product_variant.stock:
            return JsonResponse({
            'icon': 'error',
            'message': 'تعداد انتخاب شده شما بیشتر از موجودی محصول می باشد'
            })
        else:
            order_item, created = OrderItem.objects.get_or_create(is_active=True, order=order, product_variant=product_variant)
            if created:
                order_item.quantity = quantity
                order_item.save()
                return JsonResponse({
                'icon': 'success',
                'message': 'محصول به سبد خرید شما اضافه شد'
                })      
            else:
                return JsonResponse({
                'icon': 'info',
                'message': 'محصول از قبل در سبد خرید شما وجود دارد'
                })                           
    else:                
        return JsonResponse({
        'icon': 'error',
        'message': 'این ترکیب و رنگ وجود ندارد'
        })           


class AddOrderItem(View):
    def post(self, request,):
        if request.user.is_authenticated:
            data = json.loads(request.body)
            order, created = Order.objects.get_or_create(is_active=True, user=request.user, status='placed', is_paid=False)
            if created:
                order.save()          
                return add_order_item(request=request, data=data, order=order)                            
            else:
                return add_order_item(request=request, data=data, order=order)                            
        else:
            return JsonResponse({
                'icon': 'error',
                'message': 'برای افزودن به سبد خرید ابتدا باید وارد حساب کاربری خود شده باشید'
            })
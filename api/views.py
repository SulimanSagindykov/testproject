from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import (
    Category, Subcategory, Supplier, Product,
    Promotion, Favorite, CartItem, Order, OrderItem
)
from .serializers import (SupplierSerializer, ProductSerializer)
from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['GET'])
def search(request):
    query = request.GET.get('query', '')
    product_qs = Product.objects.filter(name__icontains=query)
    supplier_qs = Supplier.objects.filter(name__icontains=query)

    product_serializer = ProductSerializer(product_qs, many=True)
    supplier_serializer = SupplierSerializer(supplier_qs, many=True)

    results = []

    for product in product_serializer.data:
        results.append({
            'type': 'product',
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'image': product['image'],
        })

    for supplier in supplier_serializer.data:
        results.append({
            'type': 'distributor',
            'id': supplier['id'],
            'name': supplier['name'],
            'description': '',
            'image': supplier['logo'],
        })

    return Response({'results': results})

@api_view(['GET'])
def promotions_carousel(request):
    promotions = Promotion.objects.all()
    data = []
    for promo in promotions:
        data.append({
            'id': promo.id,
            'title': promo.title,
            'image': promo.image,
            'link': promo.link,
        })
    return Response({'promotions': data})

@api_view(['GET'])
def recommended_distributors(request):
    distributors = Supplier.objects.order_by('-rating')[:5]  # best 5 suppliers
    data = []
    for dist in distributors:
        data.append({
            'id': dist.id,
            'name': dist.name,
            'logo': dist.logo,
            'rating': dist.rating,
        })
    return Response({'distributors': data})

@api_view(['GET'])
def categories_list(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    data = []
    for category in categories:
        subcategories = category.subcategories.all()
        subcat_data = []
        for subcat in subcategories:
            subcat_data.append({
                'id': subcat.id,
                'name': subcat.name,
            })
        data.append({
            'id': category.id,
            'name': category.name,
            'subcategories': subcat_data,
        })
    return Response({'categories': data})

@api_view(['GET'])
def suppliers_by_subcategory(request, id):
    suppliers = Supplier.objects.filter(products__subcategory_id=id).distinct()
    data = []
    for supplier in suppliers:
        data.append({
            'id': supplier.id,
            'name': supplier.name,
            'logo': supplier.logo,
            'rating': supplier.rating,
        })
    return Response({'suppliers': data})

@api_view(['GET'])
def supplier_products(request, id):
    products = Product.objects.filter(supplier_id=id)
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'sku': product.sku,
            'name': product.name,
            'city': product.city,
            'image': product.image,
            'delivery_time': product.delivery_time,
        })
    return Response({'products': data})

@api_view(['POST'])
def add_to_favorites(request):
    product_id = request.data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return Response({'status': 'Product added to favorites'})

@api_view(['POST'])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    return Response({'status': 'Product added to cart'})

# --- Product Page by ID ---
@api_view(['GET'])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    characteristics = [{'name': c.name, 'value': c.value} for c in product.characteristics.all()]
    suppliers = Supplier.objects.filter(products=product)
    suppliers_data = []
    for supplier in suppliers:
        suppliers_data.append({
            'id': supplier.id,
            'name': supplier.name,
            'price': product.wholesale_price,  # Assuming price is from product
            'delivery_time': product.delivery_time,
        })
    product_data = {
        'name': product.name,
        'price': {
            'retail': product.retail_price,
            'wholesale': product.wholesale_price,
        },
        'min_order': product.min_order,
        'delivery_time': product.delivery_time,
        'city': product.city,
        'description': product.description,
        'characteristics': characteristics,
        'suppliers': suppliers_data,
    }
    return Response({'product': product_data})


@api_view(['GET'])
def get_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product', 'product__supplier')
    suppliers = {}
    for item in cart_items:
        supplier = item.product.supplier
        if supplier.id not in suppliers:
            suppliers[supplier.id] = {
                'id': supplier.id,
                'name': supplier.name,
                'products': [],
            }
        suppliers[supplier.id]['products'].append({
            'id': item.product.id,
            'name': item.product.name,
            'quantity': item.quantity,
            'price': item.product.retail_price,
            'image': item.product.image,
        })
    cart_data = {'suppliers': list(suppliers.values())}
    return Response({'cart': cart_data})

@api_view(['PATCH'])
def update_cart_item(request, id):
    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({'status': 'Quantity not provided'}, status=status.HTTP_400_BAD_REQUEST)
    cart_item = get_object_or_404(CartItem, id=id, user=request.user)
    cart_item.quantity = quantity
    cart_item.save()
    return Response({'status': 'Cart item updated'})

@api_view(['DELETE'])
def delete_cart_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id, user=request.user)
    cart_item.delete()
    return Response({'status': 'Cart item deleted'})

@api_view(['POST'])
def calculate_delivery_cost(request):
    city_id = request.data.get('city_id')
    products = request.data.get('products', [])
    # delivery cost calculation logic here
    delivery_cost = 0
    return Response({'delivery_cost': delivery_cost})

@api_view(['POST'])
def create_order(request):
    user_id = request.data.get('user_id')
    items = request.data.get('items', [])
    delivery_date = request.data.get('delivery_date')
    payment_method = request.data.get('payment_method')
    comment = request.data.get('comment', '')

    order = Order.objects.create(
        user=request.user,
        delivery_date=delivery_date,
        payment_method=payment_method,
        comment=comment
    )

    for item in items:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)
        product = get_object_or_404(Product, id=product_id)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

    CartItem.objects.filter(user=request.user).delete()

    return Response({
        'order_id': order.id,
        'status': 'Order created successfully'
    })
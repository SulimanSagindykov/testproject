from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('carousel/promotions/', views.promotions_carousel, name='promotions_carousel'),
    path('carousel/recommended-distributors/', views.recommended_distributors, name='recommended_distributors'),
    path('categories/', views.categories_list, name='categories_list'),
    path('subcategory/<int:id>/suppliers/', views.suppliers_by_subcategory, name='suppliers_by_subcategory'),
    path('supplier/<int:id>/products/', views.supplier_products, name='supplier_products'),
    path('favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('cart/', views.get_cart, name='get_cart'),  # GET method
    path('cart/', views.add_to_cart, name='add_to_cart'),  # POST method
    path('cart/product/<int:id>/', views.update_cart_item, name='update_cart_item'),  # PATCH method
    path('cart/product/<int:id>/', views.delete_cart_item, name='delete_cart_item'),  # DELETE method
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('delivery-cost/', views.calculate_delivery_cost, name='calculate_delivery_cost'),
    path('orders/', views.create_order, name='create_order'),
]
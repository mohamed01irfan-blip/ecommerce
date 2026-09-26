from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Storefront Landing
    path('', views.home, name='home'),
    path('home/', views.home, name='home_alt'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Offers (user side)
    path('offers/', views.offer_list, name='offer_list'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Search
    path('search/', views.search, name='search'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Buy Now
    path('buy-now/<int:id>/', views.buy_now, name='buy_now'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout-direct/<int:order_id>/', views.checkout_direct, name='checkout_direct'),

    # Orders (User)
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

    # ✅ Dashboard (NO dashboard/ prefix here)

    path('orders/', views.admin_orders, name='admin_orders'),
    path('orders/<int:id>/', views.admin_order_detail, name='admin_order_detail'),

    path('products/', views.admin_products, name='admin_products'),
    path('products/add/', views.admin_add_product, name='admin_add_product'),
    path('products/edit/<int:id>/', views.admin_edit_product, name='admin_edit_product'),
    path('products/delete/<int:id>/', views.admin_delete_product, name='admin_delete_product'),

    path('categories/', views.admin_categories, name='admin_categories'),
    path('categories/add/', views.admin_add_category, name='admin_add_category'),
    path('categories/edit/<int:id>/', views.admin_edit_category, name='admin_edit_category'),
    path('categories/delete/<int:id>/', views.admin_delete_category, name='admin_delete_category'),

    # ✅ FIXED OFFERS
    path('offers/admin/', views.admin_offers, name='admin_offers'),
    path('offers/admin/add/', views.admin_add_offer, name='admin_add_offer'),
    path('offers/admin/edit/<int:id>/', views.admin_edit_offer, name='admin_edit_offer'),
    path('offers/admin/delete/<int:id>/', views.admin_delete_offer, name='admin_delete_offer'),


    path('category/<int:id>/', views.category_products, name='category_products'),
]
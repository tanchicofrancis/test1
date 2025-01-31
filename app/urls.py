from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/', views.order_success, name='order_success'),
    path('products/list/', views.ProductListView.as_view(), name='product-list'),
    path('products/create/', views.product_create, name='product-create'),  
    path('products/display/', views.product_list, name='product-display'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', views.product_update, name='product-update'), 
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_customer_profile, name='update-customer-profile'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer/add/', views.add_customer, name='add_customer'),
    path('customer/update/<int:pk>/', views.update_customer, name='update_customer'),
    path('customer/delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/update/', views.update_category, name='update_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('orders/', views.order_list, name='order-list'),
    path('orders/create/', views.order_create, name='order-create'),
    path('orders/<int:pk>/update/', views.order_update, name='order-update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order-delete'),
    path('order-items/', views.order_item_list, name='order-item-list'),
    path('order-items/add/', views.order_item_create, name='order-item-create'),
    path('order-items/<int:pk>/', views.order_item_view, name='order-item-view'),  
    path('order-items/<int:pk>/edit/', views.order_item_update, name='order-item-update'),  
    path('order-items/<int:pk>/delete/', views.order_item_delete, name='order-item-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
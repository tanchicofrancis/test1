from django.contrib import admin
from .models import Post, Product, Category, Customer, Order, OrderItem

admin.site.register(Post)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

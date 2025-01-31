from django.contrib import admin
from .models import Product, Category, Customer, Order, OrderItem 

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'status', 'created_at') 
    list_filter = ('status',)  
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__email')  
    inlines = [OrderItemInline]  

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_joined')  
    search_fields = ('first_name', 'last_name', 'email', 'phone_number') 
    exclude = ('date_joined',)  
    fields = ('first_name', 'last_name', 'email', 'phone_number', 'address')  

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['first_name'].required = True
        form.base_fields['phone_number'].required = False
        form.base_fields['address'].required = False
        return form

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
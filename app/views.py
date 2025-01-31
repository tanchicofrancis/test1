from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Customer, Order, OrderItem, Category
from .forms import CustomerForm, CheckoutForm, ProductForm, OrderForm, OrderItemForm
from django.contrib import messages
import decimal
class HomePage(TemplateView):
    template_name = 'app/home.html'

class AboutPage(TemplateView):
    template_name = 'app/about.html'

class ProductListView(ListView):
    model = Product
    template_name = 'app/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'app/product_form.html'
    fields = ['name', 'price', 'stock']
    success_url = reverse_lazy('product-list')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'
    context_object_name = 'product'

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'app/product_form.html'
    fields = ['name', 'price', 'stock', 'description', 'image']
    success_url = reverse_lazy('product-display')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'app/product_delete.html'
    success_url = reverse_lazy('product-display')

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'app/customer_list.html'
    context_object_name = 'customers'

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'app/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()

class OrderItemListView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = 'app/order_item_list.html'
    context_object_name = 'order_items'

    def get_queryset(self):
        return OrderItem.objects.all()
@login_required
def profile_view(request):
    user_profile = get_object_or_404(Customer, user=request.user)
    return render(request, 'app/profile.html', {'user_profile': user_profile})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart
    total_price = sum(decimal.Decimal(item['price']) * item['quantity'] for item in cart.values())

    return JsonResponse({
        'success': True,
        'message': f'{product.name} has been added to your cart.',
        'total_price': str(total_price),
    })

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        total_price = sum(decimal.Decimal(item['price']) * item['quantity'] for item in cart.values())

        return JsonResponse({"success": True, "new_total_price": str(total_price)})

    return JsonResponse({"success": False, "message": "Product not found in cart"})

@login_required(login_url='/login/')
def cart_view(request):
    cart = request.session.get('cart', {})
    total_price = sum(decimal.Decimal(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'app/cart.html', {'cart': cart, 'total_price': total_price})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    total_price = sum(decimal.Decimal(item['price']) * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            email = form.cleaned_data.get('email')
            payment_method = form.cleaned_data['payment_method']

            if payment_method != "Cash on Delivery":
                return render(request, 'app/checkout.html', {
                    'form': form,
                    'total_price': total_price,
                    'error_message': 'Only Cash on Delivery is available as a payment method.',
                })

            customer, created = Customer.objects.get_or_create(
                user=request.user,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'email': email,
                    'address': address
                }
            )

            if not created:
                customer.first_name = first_name
                customer.last_name = last_name
                customer.phone_number = phone_number
                customer.address = address
                customer.save()

            order = Order.objects.create(
                customer=customer,
                total_price=total_price,
                status='pending'
            )

            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )

            request.session['cart'] = {}
            return redirect('order_success')

    else:
        form = CheckoutForm()

    return render(request, 'app/checkout.html', {
        'form': form,
        'total_price': total_price,
        'note': 'Cash on Delivery is the only available payment method.',
    })

@login_required
def order_success(request):
    return render(request, 'app/order_success.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'app/admin_dashboard.html')

def create_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'app/create_category.html')

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'app/category_list.html', {'categories': categories})

def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.save()
        return redirect('category_list')
    return render(request, 'app/update_category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')

def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'app/add_customer.html', {'form': form})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'app/customer_list.html', {'customers': customers})

def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'app/update_customer.html', {'form': form})

def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')
    return render(request, 'app/delete_customer.html', {'customer': customer})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'app/product_display.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-display')
    else:
        form = ProductForm()
    return render(request, 'app/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-display')
    else:
        form = ProductForm(instance=product)
    return render(request, 'app/product_update.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product-display')
    return render(request, 'app/product_delete.html', {'product': product})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'app/order_list.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order-list')
    else:
        form = OrderForm()
    return render(request, 'app/order_form.html', {'form': form})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order-list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'app/order_form.html', {'form': form, 'order': order})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order-list')
    return render(request, 'app/order_confirm_delete.html', {'order': order})

def order_item_list(request):
    order_items = OrderItem.objects.all()
    return render(request, 'app/order_item_list.html', {'order_items': order_items})

def order_item_view(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)
    return render(request, 'app/order_item_detail.html', {'item': item})

def order_item_create(request):
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order-item-list')
    else:
        form = OrderItemForm()
    return render(request, 'app/order_item_form.html', {'form': form})

def order_item_update(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('order-item-list')
    else:
        form = OrderItemForm(instance=item)
    return render(request, 'app/order_item_form.html', {'form': form})

def order_item_delete(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('order-item-list')
    return render(request, 'app/order_item_confirm_delete.html', {'item': item})

@login_required
def customer_profile(request):
    customer = Customer.objects.get(user=request.user)  
    return render(request, 'app/profile.html', {'customer': customer})

@login_required
def update_customer_profile(request):
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile') 
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'app/update_customer_profile.html', {'form': form})

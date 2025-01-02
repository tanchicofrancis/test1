from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Product 

class HomePage(TemplateView):
    template_name = 'app/home.html'

class ProductPage(TemplateView):
    template_name = 'app/product.html'

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
    template_name = 'app/product_detail.html'  # 
    context_object_name = 'product'

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'app/product_form.html'  
    fields = ['name', 'price', 'stock']
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'app/product_confirm_delete.html' 
    success_url = reverse_lazy('product-list')

class AboutPage(TemplateView):
    template_name = 'app/about.html'

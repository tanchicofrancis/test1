from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Product, Order, OrderItem

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if password2 != self.cleaned_data.get('password1'):
            raise forms.ValidationError("Passwords must match.")
        return password2

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'description', 'image']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'image': forms.ClearableFileInput() 
        }

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=False)  
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    email = forms.EmailField(required=False)  
    payment_method = forms.ChoiceField(choices=[('Cash on Delivery', 'Cash on Delivery')], required=True)

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            return 'N/A'  
        return last_name

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status']  

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']

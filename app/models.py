from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(default="Default description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Cart(models.Model):
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.customer.full_name}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.price * self.quantity

class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('canceled', 'Canceled'),
        ],
        default='pending'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Order {self.id} - {self.customer.full_name}"

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Calculate total_price from related OrderItems
        super().save(*args, **kwargs)
        self.total_price = sum(item.total_price for item in self.items.all())
        super().save(update_fields=['total_price'])

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.price * self.quantity

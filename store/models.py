from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name




# ✅ Restaurant Models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='food_images/')
    rating = models.FloatField(default=4.0)
    stock = models.IntegerField(default=10)
    
    is_offer = models.BooleanField(default=False)
    offer_name = models.CharField(max_length=100, blank=True, null=True)
    discount = models.IntegerField(default=0)
    offer_end_date = models.DateField(blank=True, null=True)

    def offer_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price

    def is_offer_active(self):
        if self.is_offer and self.offer_end_date:
            return self.offer_end_date >= timezone.now().date()
        return False

    def __str__(self):
        return self.name


class AdminUser(models.Model):
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.phone
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.food_name

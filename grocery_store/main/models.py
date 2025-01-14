from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. extend user model
class User(AbstractUser):
  USER_TYPE_CHOICES = [
      ('customer', 'Customer'),
      ('staff', 'Staff'),
  ]
  user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
  phone_number = models.CharField(max_length=15)
  
  groups = models.ManyToManyField(
    'auth.Group',
    related_name='custom_user_set',
    blank=True,
    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    verbose_name='groups',
  )
  user_permissions = models.ManyToManyField(
    'auth.Permission',
    related_name='custom_user_permissions_set',
    blank=True,
    help_text='Specific permissions for this user.',
    verbose_name='user permissions',
  )
  
  def is_customer(self):
    return self.user_type == 'customer'
  
  def is_staff(self):
    return self.user_type == 'staff'
    

# 2. product model
class Product(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  
  def __str__(self):
    return self.name

# 3. basket model
class Basket(models.Model):
  STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('denied', 'Denied'),
  )
  customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'customer'})
  product = models.ManyToManyField(Product)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
  created_at = models.DateTimeField(auto_now_add=True)
    
    
# 4. purchase history model
class PurchaseHistory(models.Model):
  customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'customer'})
  # product = models.ForeignKey(Product, on_delete=models.CASCADE)
  products = models.ManyToManyField(Product)
  purchased_at = models.DateTimeField(auto_now_add=True)
  
  def get_products(self):
    return ", ".join([product.name for product in self.products.all()])
  def get_total_price(self):
    return sum([product.price for product in self.products.all()])
  
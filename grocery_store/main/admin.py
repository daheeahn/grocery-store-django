from django.contrib import admin
from .models import User, Product, Basket, PurchaseHistory

# register user model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')

# register product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')

# register basket model
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'created_at')

# register purchase history model
@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'get_products', 'purchased_at')
    
    def get_products(self, obj):
      return ", ".join([product.name for product in obj.products.all()])
  
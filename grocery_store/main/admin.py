from django.contrib import admin
from .models import User, Product, Basket, PurchaseHistory

# 사용자 모델 등록
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')

# 제품 모델 등록
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')

# 장바구니 모델 등록
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'created_at')

# 구매 이력 모델 등록
@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'get_products', 'purchased_at')
    
    def get_products(self, obj):
      return ", ".join([product.name for product in obj.products.all()])
  
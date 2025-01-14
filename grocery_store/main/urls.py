from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # list of products
    path('basket/', views.basket_view, name='basket_view'),  # customer basket view
    path('basket/add/<int:product_id>/', views.add_to_basket, name='add_to_basket'),  # add to basket
    path('purchase-history/', views.purchase_history, name='purchase_history'),  # purchase history

    path('staff/products/', views.staff_product_list, name='staff_product_list'),  # staff product list
    path('staff/products/add/', views.add_product, name='add_product'),  # add product
    path('staff/baskets/', views.staff_basket_list, name='staff_basket_list'),  # customer basket management
    path('staff/customers/', views.customer_information, name='customer_information'),  # customer information
    
    path('basket/<int:basket_id>/approve/', views.approve_basket, name='approve_basket'),
    path('basket/<int:basket_id>/deny/', views.deny_basket, name='deny_basket'),
    
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
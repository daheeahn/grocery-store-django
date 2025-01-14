from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Basket, PurchaseHistory, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # set default user type to customer
            user.user_type = 'customer'
            user.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def is_customer(user):
    return user.user_type == 'customer'

def is_staff(user):
    return user.user_type == 'staff'

# 1. view product list
def product_list(request):
    products = Product.objects.all()
    # return render(request, 'main/product_list.html', {'products': products, 'user': request.user})
    return render(request, 'main/product_list.html', {'products': products})

# 2. view basket
@login_required
@user_passes_test(is_customer)
def basket_view(request):
    basket = Basket.objects.filter(customer=request.user, status='pending').order_by('-created_at').first()
    return render(request, 'main/basket_view.html', {'basket': basket})

# 3. add product to basket
@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket, created = Basket.objects.get_or_create(customer=request.user, status='pending')
    basket.product.add(product)
    return redirect('basket_view')

# 4. view purchase history
@login_required
def purchase_history(request):
    history = PurchaseHistory.objects.filter(customer=request.user)
    return render(request, 'main/purchase_history.html', {'history': history})

# 5. view staff product list
@user_passes_test(is_staff)
def staff_product_list(request):
    products = Product.objects.all()
    return render(request, 'main/staff_product_list.html', {'products': products})

# 6. add product (staff only)
@user_passes_test(is_staff)
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        Product.objects.create(name=name, price=price)
        return redirect('staff_product_list')
    return render(request, 'main/add_product.html')

# 7. customer basket management (staff only)
@user_passes_test(is_staff)
def staff_basket_list(request):
    baskets = Basket.objects.filter(status='pending')
    return render(request, 'main/staff_basket_list.html', {'baskets': baskets})

# 8. approve basket (staff only)
@user_passes_test(is_staff)
def approve_basket(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    basket.status = 'approved'  # change basket status to 'approved'
    basket.save()
    
    purchase_history = PurchaseHistory.objects.create(customer=basket.customer)
    purchase_history.products.set(basket.product.all())
    
    return redirect('staff_basket_list')  # redirect to staff basket list

# 9. deny basket (staff only)
@user_passes_test(is_staff)
def deny_basket(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    basket.status = 'denied'  # change basket status to 'denied'
    basket.save()
    return redirect('staff_basket_list')  # redirect to staff basket list

# 10. view customer purchase history
@login_required
@user_passes_test(is_staff)
def customer_information(request):
    customers = User.objects.filter(user_type='customer')
    purchase_histories = {customer: PurchaseHistory.objects.filter(customer=customer) for customer in customers}
    return render(request, 'main/customer_information.html', {'purchase_histories': purchase_histories})
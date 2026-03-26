from django.shortcuts import render
from .models import Food, Category
from .models import AdminUser
from .forms import FoodForm
from .forms import Food
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Order, OrderItem
import random
from django.utils import timezone



def home(request):
    return render(request, 'home.html')
# Create your views here.
def contact(request):
    return render(request, "contact.html")

def menu(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'menu.html', context)

def admin_login(request):
    if request.method == "POST":
        phone = request.POST.get('phone')

        # ✅ create or get admin
        user, created = AdminUser.objects.get_or_create(phone=phone)

        # ✅ store session
        request.session['admin_id'] = user.id

        return redirect('dashboard')

    return render(request, 'admin_login.html')

from .models import Food, Category

def dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    categories = Category.objects.all()
    foods = Food.objects.all()
    orders = Order.objects.all().order_by('-created_at')

    return render(request, 'dashboard.html', {
        'categories': categories,
        'foods': foods,
        'orders': orders
    })

    
def add_food(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    form = FoodForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'add_food.html', {'form': form})

def update_food(request, id):
    food = get_object_or_404(Food, id=id)

    form = FoodForm(request.POST or None, request.FILES or None, instance=food)

    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'add_food.html', {'form': form})

def delete_food(request, id):
    food = get_object_or_404(Food, id=id)
    food.delete()
    return redirect('dashboard')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
from django.shortcuts import redirect, get_object_or_404
from .models import Food

def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    food = get_object_or_404(Food, id=id)

    if str(id) in cart:
        cart[str(id)]['quantity'] += 1
    else:
        cart[str(id)] = {
            'name': food.name,
            'price': float(food.price),
            'quantity': 1,
            'image': food.image.url
        }

    request.session['cart'] = cart

    return redirect(request.META.get('HTTP_REFERER', 'menu'))

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = request.session.get('cart', {})
    total = 0

    for item in cart.values():
        total += item['price'] * item['quantity']

    return render(request, 'cart.html', {'cart': cart, 'total': total})

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')


def user_logout(request):
    logout(request)

    # ✅ clear cart
    request.session['cart'] = {}

    return redirect('home')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return redirect('payment')


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders.html', {'orders': orders})

def update_cart(request, id, action):
    cart = request.session.get('cart', {})

    if str(id) in cart:

        if action == 'increase':
            cart[str(id)]['quantity'] += 1

        elif action == 'decrease':
            cart[str(id)]['quantity'] -= 1

            # remove if quantity becomes 0
            if cart[str(id)]['quantity'] <= 0:
                del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')

def payment(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('menu')

    total = 0
    for item in cart.values():
        total += item['price'] * item['quantity']

    return render(request, 'payment.html', {'total': total})

def place_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('menu')

    total = 0

    # ✅ Calculate total
    for item in cart.values():
        total += item['price'] * item['quantity']

    # ✅ Create Order
    order = Order.objects.create(
        user=request.user,
        total=total
    )

    # ✅ Save Order Items + Reduce Stock
    for item in cart.values():
        try:
            food = Food.objects.get(name=item['name'])

            # 🔻 Reduce stock
            food.stock -= item['quantity']
            if food.stock < 0:
                food.stock = 0
            food.save()

        except Food.DoesNotExist:
            food = None  # safety

        OrderItem.objects.create(
            order=order,
            food_name=item['name'],
            price=item['price'],
            quantity=item['quantity']
        )

    # ✅ Clear cart
    request.session['cart'] = {}

    return render(request, 'success.html', {'total': total})

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if str(entered_otp) == str(session_otp):
            phone = request.session.get('phone')
            user = AdminUser.objects.get(phone=phone)

            request.session['admin_id'] = user.id

            return redirect('dashboard')
        else:
            return render(request, 'verify_otp.html', {
                'error': 'Invalid OTP'
            })

    return render(request, 'verify_otp.html')

def admin_logout(request):
    request.session.flush()   # clears admin session
    return redirect('home')

def menu(request):
    query = request.GET.get('q')

    if query:
        foods = Food.objects.filter(name__icontains=query)
    else:
        foods = Food.objects.all()

    categories = Category.objects.all()

    return render(request, 'menu.html', {
        'foods': foods,
        'categories': categories
    })
    
from django.utils import timezone

def offers(request):
    today = timezone.now().date()

    foods = Food.objects.filter(is_offer=True,offer_end_date__gte=today )

    return render(request, 'offers.html', {'foods': foods})

from django.utils import timezone
from .models import Order, OrderItem, Food

def admin_report(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    today = timezone.now().date()

    # ✅ today's orders
    orders = Order.objects.filter(created_at__date=today)

    # ✅ total sales
    total_sales = sum(order.total for order in orders)

    # ✅ sold items today
    items = OrderItem.objects.filter(order__created_at__date=today)

    # ✅ inventory (all foods)
    foods = Food.objects.all()

    return render(request, 'admin_report.html', {
        'orders': orders,
        'items': items,
        'total_sales': total_sales,
        'foods': foods
    })
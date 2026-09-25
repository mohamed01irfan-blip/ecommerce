from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from .models import Product, Cart, Order, OrderItem, Offer, Category
from .forms import ProductForm, CheckoutForm
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order
from django.http import HttpResponse
from .models import Offer
from django.shortcuts import render
from .models import Product, Category, ProductImage




def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def offer_list(request):
    offers = Offer.objects.all()
    return render(request, 'shop/offer_list.html', {'offers': offers})

def orders(request):
    return HttpResponse("Orders Page Working ✅")




def admin_order_detail(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == "POST":
        status = request.POST.get('status')
        order.status = status
        order.save()
        return redirect('shop:admin_order_detail', id=order.id)

    return render(request, 'shop/admin_order_detail.html', {'order': order})



def admin_orders(request):
    orders = Order.objects.all()
    return render(request, 'shop/admin_orders.html', {'orders': orders})


def admin_edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')   # 🔥 ADD THIS LINE

        category_id = request.POST.get('category')
        new_category = request.POST.get('new_category')

        if new_category:
            category_obj = Category.objects.create(name=new_category)
            product.category = category_obj
        elif category_id:
            product.category_id = category_id

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()

        for img in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=img)

        return redirect('shop:admin_products')

    return render(request, 'shop/admin_edit_product.html', {
        'product': product,
        'categories': categories
    })


# ------------------- ADMIN CHECK -------------------
def is_admin(user):
    return user.is_superuser

@login_required
def checkout_direct(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        customer_name = (request.POST.get('customer_name') or request.POST.get('full_name') or '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        screenshot = request.FILES.get('payment_screenshot')

        if not all([customer_name, email, phone, address, screenshot]):
            return render(request, 'shop/checkout.html', {
                'order': order,
                'direct_buy': True,
                'error': 'All fields and payment screenshot are required!'
            })

        order.customer_name = customer_name
        order.email = email
        order.phone = phone
        order.address = address
        order.payment_screenshot = screenshot
        order.status = 'confirmed'
        order.save()

        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('shop:order_success', order_id=order.id)

    return render(request, 'shop/checkout.html', {
        'order': order,
        'direct_buy': True
    })


def admin_delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('shop:admin_products')


# ------------------- ORDER DETAIL -------------------
@login_required
def order_detail(request, id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=id)
    else:
        order = get_object_or_404(Order, id=id, user=request.user)

    return render(request, 'shop/order_detail.html', {
        'order': order
    })
# ------------------- BUY NOW (FIXED) -------------------
@login_required
def buy_now(request, id):
    product = get_object_or_404(Product, id=id)

    # Create Order
    order = Order.objects.create(
        user=request.user,
        customer_name=request.user.username,
        email=request.user.email or "test@gmail.com",
        phone="0000000000",
        address="Default Address",
        total_amount=product.price,
        payment_screenshot="default.jpg"
    )

    # Create Order Item
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        price=product.price
    )

    return redirect('shop:checkout_direct', order_id=order.id)


# ------------------- SEARCH -------------------
def search(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'shop/search.html', {
        'products': products,
        'query': query
    })


# ------------------- HOME -------------------
def home(request):
    products = Product.objects.all()
    offers = Offer.objects.filter(is_active=True)
    categories = Category.objects.all()

    return render(request, 'shop/home.html', {
        'products': products,
        'offers': offers,
        'categories': categories
    })


# ------------------- AUTH -------------------
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('shop:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('shop:signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('shop:signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('shop:home')

    return render(request, 'shop/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('shop:home')
        else:
            messages.error(request, 'Invalid login!')

    return render(request, 'shop/login.html')


def logout_view(request):
    logout(request)
    return redirect('shop:home')


# ------------------- CART -------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('shop:home')


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.get_total() for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('shop:cart')


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('shop:cart')


# ------------------- CHECKOUT -------------------
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, 'Cart is empty!')
        return redirect('shop:cart')

    total = sum(item.get_total() for item in cart_items)

    if request.method == 'POST':
        customer_name = (request.POST.get('customer_name') or request.POST.get('full_name') or '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        screenshot = request.FILES.get('payment_screenshot')

        if not all([customer_name, email, phone, address, screenshot]):
            return render(request, 'shop/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'error': 'All fields and payment screenshot are required!'
            })

        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            email=email,
            phone=phone,
            address=address,
            total_amount=total,
            payment_screenshot=screenshot,
            status='confirmed'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('shop:order_success', order_id=order.id)

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_orders.html', {'orders': orders})


# ------------------- ADMIN -------------------
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    recent_orders = Order.objects.all()[:5]  # 🔥 get latest 5 orders

    context = {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'total_revenue': Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0,
        'recent_orders': recent_orders,  # ✅ ADD THIS
    }

    return render(request, 'shop/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_products(request):
    products = Product.objects.all()
    return render(request, 'shop/admin_products.html', {'products': products})


@login_required
@user_passes_test(is_admin)
def admin_add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('shop:admin_categories')

    return render(request, 'shop/admin_add_category.html')


@login_required
@user_passes_test(is_admin)
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'shop/admin_categories.html', {'categories': categories})


@login_required
@user_passes_test(is_admin)
def admin_add_offer(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')

        Offer.objects.create(title=title, image=image)

        return redirect('shop:admin_offers')

    return render(request, 'shop/admin_add_offer.html')


@login_required
@user_passes_test(is_admin)
def admin_offers(request):
    offers = Offer.objects.all()
    return render(request, 'shop/admin_offers.html', {'offers': offers})
    


@login_required
@user_passes_test(is_admin)
def admin_add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', '').strip()
        stock = request.POST.get('stock', '').strip()
        category_id = request.POST.get('category', '').strip()
        new_category = request.POST.get('new_category', '').strip()

        # Support both existing category selection and new category creation
        category = None
        if new_category:
            category, _ = Category.objects.get_or_create(name=new_category)
        elif category_id:
            try:
                category = Category.objects.get(id=int(category_id))
            except (Category.DoesNotExist, ValueError, TypeError):
                messages.error(request, 'Selected category does not exist.')
                categories = Category.objects.all()
                return render(request, 'shop/admin_add_product.html', {'categories': categories})
        else:
            messages.error(request, 'Please select an existing category or enter a new category.')
            categories = Category.objects.all()
            return render(request, 'shop/admin_add_product.html', {'categories': categories})

        # Parse stock quantity
        try:
            stock_qty = int(stock) if stock else 0
        except ValueError:
            stock_qty = 0

        # Handle multiple uploaded images
        images = request.FILES.getlist('images')
        primary_image = images[0] if images else request.FILES.get('image')

        # Create product
        product = Product.objects.create(
            name=name,
            price=price,
            stock=stock_qty,
            category=category,
            image=primary_image
        )

        # Save additional gallery images
        for img in images:
            ProductImage.objects.create(
                product=product,
                image=img
            )

        messages.success(request, f'Product "{name}" added successfully!')
        return redirect('shop:admin_products')

    categories = Category.objects.all()
    return render(request, 'shop/admin_add_product.html', {
        'categories': categories
    })

@login_required
@user_passes_test(is_admin)
def admin_edit_offer(request, id):
    offer = Offer.objects.get(id=id)

    if request.method == 'POST':
        offer.title = request.POST.get('title')
        offer.description = request.POST.get('description')

        # 🔥 ADD THIS LINE HERE
        offer.is_active = True if request.POST.get('is_active') else False

        # image update (optional)
        if request.FILES.get('image'):
            offer.image = request.FILES.get('image')

        offer.save()
        return redirect('shop:admin_offers')

    return render(request, 'shop/admin_edit_offer.html', {'offer': offer})

@login_required
@user_passes_test(is_admin)
def admin_delete_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
    offer.delete()
    return redirect('shop:admin_offers')

def category_products(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)

    return render(request, 'shop/category_products.html', {
        'category': category,
        'products': products
    })
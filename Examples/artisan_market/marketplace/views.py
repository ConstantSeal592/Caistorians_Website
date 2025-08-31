from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .utils.basket import add_to_basket, remove_from_basket

from .models import Product, Basket, BasketItem, SellerVideo, ProductView, ArtistProfile
from .forms import ProductForm, SellerVideoForm, ArtistProfileForm
from .utils.basket import *

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# Product list with search, sorting, pagination
def product_list(request):
    products = Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))

    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'title_asc':
        products = products.order_by('title')
    elif sort == 'title_desc':
        products = products.order_by('-title')
    else:
        products = products.order_by('-id')  # newest first fallback

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.page(1)

    return render(request, 'marketplace/product_list.html', {
        'products': page_obj,
        'query': query or '',
        'sort': sort,
    })


def personalized_product_list(request):
    user = request.user if request.user.is_authenticated else None

    if user:
        categories = ProductView.objects.filter(user=user).values_list('product__category', flat=True)
        products = Product.objects.filter(category__in=categories).distinct() if categories else Product.objects.all()
    else:
        products = Product.objects.all()

    products = products.order_by('?')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'products_html': '', 'has_next': False})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_html = render_to_string('marketplace/partials/product_list_items.html', {'products': page_obj})
        return JsonResponse({
            'products_html': products_html,
            'has_next': page_obj.has_next()
        })

    return render(request, 'marketplace/for_you.html', {'page_obj': page_obj})


# Create a new product (logged-in sellers only)
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            form.save_m2m()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'marketplace/create_product.html', {'form': form})


# Product detail view
class ProductDetailView(DetailView):
    model = Product
    template_name = 'marketplace/product_detail.html'
    context_object_name = 'product'


# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('edit_profile')
    else:
        form = UserCreationForm()
    return render(request, 'marketplace/register.html', {'form': form})


# Login view
class CustomLoginView(LoginView):
    template_name = 'marketplace/login.html'


# Upload seller video
@login_required
def upload_seller_video(request):
    if request.method == 'POST':
        form = SellerVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.seller = request.user
            video.save()
            return redirect('view_seller_profile', username=request.user.username)
    else:
        form = SellerVideoForm()
    return render(request, 'marketplace/upload_seller_video.html', {'form': form})


@login_required
def my_profile(request):
    profile = getattr(request.user, 'artistprofile', None)
    products = Product.objects.filter(seller=request.user)
    videos = SellerVideo.objects.filter(seller=request.user)
    return render(request, 'marketplace/profile_detail.html', {
        'profile': profile,
        'products': products,
        'videos': videos,
        'profile_user': request.user,  # pass current user as profile_user for template consistency
    })
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = getattr(user, 'artistprofile', None)
    products = Product.objects.filter(seller=user)
    videos = SellerVideo.objects.filter(seller=request.user)
    return render(request, 'marketplace/profile_detail.html', {
        'profile_user': user,
        'profile': profile,
        'products': products,
        'videos': videos,
    })    


# Public seller profile by username
def view_seller_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = getattr(user, 'artistprofile', None)
    products = Product.objects.filter(seller=user)
    videos = SellerVideo.objects.filter(seller=user)
    return render(request, 'marketplace/view_seller_profile.html', {
        'profile_user': user,
        'profile': profile,
        'products': products,
        'videos': videos,
    })

# Edit profile view
@login_required
def edit_profile(request):
    profile = getattr(request.user, 'artistprofile', None)

    if request.method == 'POST':
        form = ArtistProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            artist_profile = form.save(commit=False)
            artist_profile.user = request.user
            artist_profile.save()
            return redirect('my_profile')
    else:
        form = ArtistProfileForm(instance=profile)

    return render(request, 'marketplace/edit_profile.html', {
        'form': form,
    })

from django.views.decorators.http import require_POST
from .utils.basket import get_user_basket

@require_POST
def update_basket(request):
    basket_data, source = get_user_basket(request)

    if source == 'db':
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    item = BasketItem.objects.get(basket=basket_data, product_id=product_id)
                    if quantity > 0:
                        item.quantity = quantity
                        item.save()
                    else:
                        item.delete()
                except (ValueError, BasketItem.DoesNotExist):
                    continue
    else:
        session_basket = request.session.get('basket', {})
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity > 0:
                        session_basket[product_id] = quantity
                    else:
                        session_basket.pop(product_id, None)
                except ValueError:
                    continue
        request.session['basket'] = session_basket

    return redirect('view_basket')

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from marketplace.models import Product
from .utils.basket import add_to_basket as basket_add

from django.views.decorators.http import require_http_methods

def add_to_basket(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        basket_add(request, product.id)
        return redirect('view_basket')
    else:
        # If accessed via GET, just redirect to product detail or basket
        return redirect('product_detail', pk=pk)
def remove_from_basket_view(request, pk):
    remove_from_basket(request, pk)
    return redirect('view_basket')

@login_required
def manage_listings(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'marketplace/manage_listings.html', {'products': products})

def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Store Buy Now data in session for one-time checkout
    request.session['buy_now'] = {
        'product_id': product.pk,
        'quantity': 1
    }

    return redirect('checkout')


def view_basket(request):
    items = get_basket_items(request)      # get basket items, handles both auth and anon users
    total = get_basket_total(request)      # get total price
    return render(request, 'marketplace/basket.html', {
        'items': items,
        'total': total,
    })

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'marketplace/product_edit.html', {'form': form, 'request': request})



from django.contrib import messages

@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('manage_listings')

@login_required
def remove_from_basket(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = get_object_or_404(Basket, user=request.user)
    basket_item = BasketItem.objects.filter(basket=basket, product=product).first()

    if basket_item:
        basket_item.delete()
        messages.success(request, f'Removed {product.title} from your basket.')
    else:
        messages.warning(request, f'{product.title} was not in your basket.')

    return redirect('view_basket')


@login_required
def update_basket_item(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=pk)
        basket = get_object_or_404(Basket, user=request.user)
        basket_item = BasketItem.objects.filter(basket=basket, product=product).first()

        if basket_item:
            if quantity > 0:
                basket_item.quantity = quantity
                basket_item.save()
                messages.success(request, f'Updated {product.title} quantity to {quantity}.')
            else:
                basket_item.delete()
                messages.success(request, f'Removed {product.title} from your basket.')
        else:
            messages.warning(request, f'{product.title} was not in your basket.')

    return redirect('view_basket')


def checkout(request):
    buy_now_data = request.session.get('buy_now', None)
    if buy_now_data:
        # User is buying one product directly
        product = get_object_or_404(Product, pk=buy_now_data['product_id'])
        quantity = buy_now_data.get('quantity', 1)

        # You can prepare a fake basket item list just with this product
        basket_items = [{'product': product, 'quantity': quantity, 'total_price': product.price * quantity}]
        total_price = product.price * quantity
    else:
        basket = get_object_or_404(Basket, user=request.user)
        basket_items = BasketItem.objects.filter(basket=basket)
        total_price = sum(item.product.price * item.quantity for item in basket_items)

    if request.method == 'POST':
        # Process payment/order here
        if buy_now_data:
            # Clear Buy Now session
            del request.session['buy_now']
        else:
            # Clear basket items
            basket_items.delete()

        messages.success(request, 'Thank you for your purchase! Your order has been placed.')
        return redirect('checkout_confirmation')

    return render(request, 'marketplace/checkout.html', {
        'basket_items': basket_items,
        'total_price': total_price,
    })
def checkout_confirmation(request):
    return render(request, 'marketplace/confirmation.html')
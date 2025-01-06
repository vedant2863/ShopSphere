from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cart, CartItem
from product.models import Product  
from django.contrib.auth.decorators import login_required

# Helper function to get or create a cart for the user
def get_or_create_cart(user):
    # Create or retrieve the cart based on the logged-in user
    cart, created = Cart.objects.get_or_create(user=user)
    return cart,created


@login_required
def view_cart(request):
    # Get or create the cart for the logged-in user
    cart = get_or_create_cart(request.user)  # Use request.user directly
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the cart. If the product already exists in the cart,
    increment its quantity.
    """
    product = get_object_or_404(Product, id=product_id)  # Ensure product exists

    # Retrieve or create the cart for the logged-in user
    cart, _ = get_or_create_cart(request.user)  # Correctly handle unpacking

    # Get or create the CartItem for this product in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # If the item already exists in the cart, increase its quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:view_cart')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart:view_cart')

@login_required
def update_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)

    # Get the updated quantity from the request
    quantity = int(request.POST.get('quantity'))
    cart_item.quantity = quantity
    cart_item.save()

    return redirect('cart:view_cart')


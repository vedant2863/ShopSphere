import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Helper function to get or create a cart for the user
def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def view_cart(request):
    cart = get_or_create_cart(request.user)  # Get the user's cart
    return render(request, "cart/cart.html", {"cart": cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = get_or_create_cart(request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1  # Increment quantity if item already exists in the cart
    cart_item.save()

    return redirect(request.META.get("HTTP_REFERER", "product:product_list"))


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect("cart:view_cart")


@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == "POST":
        quantity = request.POST.get("quantity")

        # Validate the quantity input
        if quantity and quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()

        return redirect("cart:view_cart")
    return JsonResponse({"error": "Invalid request"}, status=400)


# Handle AJAX for updating cart via POST request
@login_required
def update_cart_ajax(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == "POST":
        data = json.loads(request.body)
        quantity = data.get("quantity")

        # Validate the quantity
        if quantity and quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()

            return JsonResponse(
                {
                    "success": True,
                    "total_price": cart_item.total_price,
                    "cart_total": cart_item.cart.total_cost,
                }
            )
        return JsonResponse(
            {"success": False, "message": "Invalid quantity"}, status=400
        )

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

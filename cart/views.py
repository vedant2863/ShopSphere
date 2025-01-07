# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


# Helper function to get or create a cart for the user
def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def view_cart(request):
    cart = get_or_create_cart(request.user)  # Get only the cart
    return render(request, "cart/cart.html", {"cart": cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request.user)  # Unpack only cart

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
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
        if quantity and quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        return redirect("cart:view_cart")
    return JsonResponse({"error": "Invalid request"}, status=400)


# Handle AJAX for updating cart via POST request
@login_required
def update_cart_item_quantity(request, cart_item_id):
    if request.method == "POST":
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            quantity = int(data.get("quantity", 0))  # Parse as integer

            # Validate quantity
            if quantity < 1:
                return JsonResponse(
                    {"success": False, "message": "Quantity must be at least 1"},
                    status=400,
                )

            # Fetch cart item for the logged-in user
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)

            # Update quantity and save
            cart_item.quantity = quantity
            cart_item.save()

            # Return updated prices
            return JsonResponse(
                {
                    "success": True,
                    "total_price": cart_item.total_price,
                    "cart_total": cart_item.cart.total_cost,
                }
            )

        except CartItem.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Cart item not found"}, status=404
            )
        except ValueError:
            return JsonResponse(
                {"success": False, "message": "Invalid quantity format"}, status=400
            )
    return JsonResponse(
        {"success": False, "message": "Invalid request method"}, status=400
    )

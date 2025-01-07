from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required


@login_required
def create_order(request):
    cart = Cart.objects.get(user=request.user)

    if cart.cart_items.count() == 0:
        return redirect("cart:view_cart")

    # Create an order
    order = Order.objects.create(
        user=request.user,
        total_cost=cart.total_cost,
        status="Pending",
    )

    # Create order items from cart items
    for item in cart.cart_items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    # Clear the cart after order creation
    cart.cart_items.all().delete()

    return redirect("orders:order_summary", order_id=order.id)


@login_required
def order_summary(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "orders/order_summary.html", {"order": order})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.models import Cart
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


def cart_view(request):
    cart = Cart.objects.get(user=request.user)

    if not cart.order:
        # Create or retrieve an Order instance
        total_cost = sum(
            item.product.price * item.quantity for item in order.cart_items.all()
        )
        order = Order.objects.create(user=request.user, total_cost=total_cost)
        cart.order = order
        cart.save()

    context = {
        "cart": cart,
    }
    return render(request, "cart/cart.html", context)


@login_required
def create_order(request):
    try:
        # Get the cart for the logged-in user
        cart = Cart.objects.get(user=request.user)

        if cart.cart_items.count() == 0:
            return redirect(
                "cart:view_cart"
            )  # If the cart is empty, redirect back to the cart page

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

        # Redirect to order summary page
        return redirect("orders:order_summary", order_id=order.id)

    except Cart.DoesNotExist:
        raise Http404("Cart not found")


@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Calculate total price for each order item and add it to the context
    for item in order.items.all():
        item.total_price = item.quantity * item.price

    return render(request, "orders/order_summary.html", {"order": order})


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, "Order status updated successfully.")
        else:
            messages.error(request, "Invalid status selected.")

    return HttpResponseRedirect(reverse("orders:order_summary", args=[order.id]))

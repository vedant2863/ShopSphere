import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Payment
from order.models import Order
from django.http import JsonResponse

# Razorpay client setup
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def initiate_payment(request, order_id):
    # Fetch the order
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Initialize Razorpay client
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    # Ensure total_cost is not None
    if order.total_cost is None:
        order.total_cost = 0
        order.save()

    # Razorpay amount is in paise (multiply by 100)
    amount_in_paise = int(order.total_cost * 100)

    try:
        # Create a Razorpay order
        razorpay_order = client.order.create(
            {
                "amount": amount_in_paise,  # Amount in paise
                "currency": "INR",
                "receipt": str(order.id),
                "payment_capture": 1,  # Automatic capture
            }
        )

        # Save Razorpay order ID in the database
        order.razorpay_order_id = razorpay_order["id"]
        order.save()

        context = {
            "order": order,
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "amount": order.total_cost,  # Show amount in INR
        }
        return render(request, "payment/payment_page.html", context)

    except razorpay.errors.BadRequestError as e:
        return JsonResponse(
            {"error": "Invalid Razorpay request: " + str(e)}, status=400
        )
    except razorpay.errors.AuthenticationError:
        return JsonResponse(
            {"error": "Authentication with Razorpay failed."}, status=401
        )
    except Exception as e:
        return JsonResponse({"error": "An error occurred: " + str(e)}, status=500)


@login_required
def payment_success(request):
    payment_id = request.GET.get("payment_id")
    razorpay_order_id = request.GET.get("razorpay_order_id")
    razorpay_signature = request.GET.get("razorpay_signature")

    # Fetch payment details from the Payment model
    payment = Payment.objects.get(transaction_id=razorpay_order_id)

    # Verify the payment signature
    params_dict = {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": payment_id,
        "razorpay_signature": razorpay_signature,
    }

    try:
        client.utility.verify_payment_signature(params_dict)
        payment.status = Payment.SUCCESS
        payment.save()

        # Redirect to a success page
        return redirect("orders:order_summary", order_id=payment.order.id)

    except razorpay.errors.SignatureVerificationError:
        payment.status = Payment.FAILED
        payment.save()

        # Redirect to a failure page
        return redirect("payments:payment_failed", payment_id=payment.id)


@login_required
def payment_failed(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    return render(request, "payments/payment_failed.html", {"payment": payment})

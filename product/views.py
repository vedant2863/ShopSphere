from .models import Product
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login


# Create your views here.


def product_list(request):
    products = Product.objects.all()
    return render(request, "product/product_list.html", {"products": products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, "product/product_detail.html", {"product": product})


# auth views
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            return redirect("login")  # Redirect to the login page or dashboard
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})

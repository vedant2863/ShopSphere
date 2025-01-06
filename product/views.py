from django.shortcuts import render
from .models import Product

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products':products})

def product_detail(request, id, slug):
    product = Product.objects.get(id=id)
    return render(request, 'product/product_detail.html', {'product':product})
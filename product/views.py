from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products':products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'product/product_detail.html', {'product': product})

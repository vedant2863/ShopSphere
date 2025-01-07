from django.db import models
from product.models import Product
from order.models import Order
from django.conf import settings


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.OneToOneField(
        Order, null=True, blank=True, on_delete=models.SET_NULL
    )

    @property
    def total_cost(self):
        return sum(item.total_price for item in self.cart_items.all())


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price

from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("initiate/<int:order_id>/", views.initiate_payment, name="initiate_payment"),
    path("success/", views.payment_success, name="payment_success"),
    path("failed/<int:payment_id>/", views.payment_failed, name="payment_failed"),
]

from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.create_order, name="create_order"),
    path("<int:order_id>/summary/", views.order_summary, name="order_summary"),
    path(
        "<int:order_id>/update-status/",
        views.update_order_status,
        name="update_order_status",
    ),
]

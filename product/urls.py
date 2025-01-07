from django.contrib.auth import views as auth_views
from . import views
from django.urls import path


app_name = "product"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    # Auth URLs
    path("register/", views.register, name="register"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="registration/logged_out.html",
            next_page="/product",
        ),
        name="logout",
    ),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    # Password Reset URLs using Django's built-in views
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Home page
    path("home/", views.home, name="home"),
]

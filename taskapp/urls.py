from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_user, name="register"),
    path("login", views.login_user, name="login"),
    path("loan", views.loan_approval, name="loan")
]

from django.urls import path, re_path
from login import views


app_name = "login"

urlpatterns = [
    path("", views.register.as_view(), name = 'register'),
    path("Login/", views.loginView.as_view(), name = 'login'),
    path("logout/", views.logoutView.as_view(), name = 'logout'),
    path("profile/", views.createProfile.as_view(), name = 'addprofile'),
    path('<int:pk>/profileUpdate/', views.updateProfile.as_view(), name = 'updateprofile' ),





]

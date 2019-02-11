from django.urls import path, re_path
from login import views


app_name = "login"

urlpatterns = [

    path("register/", views.register.as_view(), name = 'register'),
    path("Login/", views.loginView.as_view(), name = 'login'),
    path("logout/", views.logoutView.as_view(), name = 'logout'),
    path("add/", views.createProfile.as_view(), name = 'addprofile'),
    path("<int:pk>/update/", views.updateProfile.as_view(), name = 'updateprofile'),
]

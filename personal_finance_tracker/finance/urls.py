from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name="finance"

urlpatterns = [
    path("home/<str:name>",views.home, name="home"),
    path("register_view", views.register_view, name="register_view"),
    path("login_view", views.login_view, name="login_view"),
    path("reset_password_view", views.reset_password_view, name="forget_password"),
    path("reset_password", views.reset_password, name="reset_password"),

    # Direct approach to login 

    # # Login URL
    # path("login/", auth_views.LoginView.as_view(), name='login'),

    # # Logout URL

    # path("logout/", auth_views.LoginView.as_view(), name='logout'),

    #  Manual login and log out 

    path("register", views.register, name="register"),
    path("login",views.Login, name='login'),
    path('logout', views.Logout, name="logout"),

    # working with data 

    path('manage_transactions', views.manage_transaction, name="manage_transactions")
    
]
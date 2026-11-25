
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import (
    dashboard,
    customer_dashboard,
    register,
    profile,
    edit_profile,
    change_password,
)


urlpatterns = [

    # Django Admin
    path(
        'admin/',
        admin.site.urls
    ),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Register
    path(
        'register/',
        register,
        name='register'
    ),

    # Admin / Main Dashboard
    path(
        '',
        dashboard,
        name='dashboard'
    ),

    # Customer Dashboard
    path(
        'customer/dashboard/',
        customer_dashboard,
        name='customer_dashboard'
    ),

    # User Profile
    path(
        'profile/',
        profile,
        name='profile'
    ),

    # Edit Profile
    path(
        'profile/edit/',
        edit_profile,
        name='edit_profile'
    ),

    # Change Password
    path(
        'profile/change-password/',
        change_password,
        name='change_password'
    ),

    # Chicken Management
    path(
        'chickens/',
        include('chickens.urls')
    ),

    # Egg Production Management
    path(
        'production/',
        include('production.urls')
    ),

    # Feed Management
    path(
        'feed/',
        include('feed.urls')
    ),

    # Health Management
    path(
        'health/',
        include('health.urls')
    ),

    # Forgot Password
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'
    ),

    # Password Reset Email Sent
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Set New Password
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # Password Reset Complete
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # Orders Management
    path(
        'orders/',
        include('orders.urls')
    ),
]

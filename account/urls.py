from django.urls import path
from . import views

urlpatterns = [


    path('register', views.register, name ='register'),


    #email verification URL's

    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name ='email-verification'),


    path('email-verification-sent', views.email_verification_sent, name ='email-verification-sent'),


    path('email-verification-success', views.email_verification_success, name ='email-verification-success'),


    path('email-verification-failed', views.email_verification_failed, name ='email-verification-failed'),




    # Login / Logout

    path('my-login', views.my_login, name='my-login'),


    path('user-logout', views.user_logout, name='user-logout'),


    # Dashboard / profile urls

    path('dashboard', views.dashboard, name='dashboard'),

    path('profile-management', views.profile_management, name='profile-management'),

    path('delete-account', views.delete_account, name='delete-account'),





]
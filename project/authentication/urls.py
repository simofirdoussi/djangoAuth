from django import views
from django.urls import path
from . import views
from authentication.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    #registration view
    path('register/', views.signup, name='register'),

    path('', views.home, name='home'),
    path('logout/', views.logoutpage, name='logout'),

    path("password_reset/", views.password_reset_request, name="password_reset"),

    #activation urls
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('activate-success/', views.activate_success, name='activate-success'), 
    path('please-activate/', views.activate_success, name='please-activate'),  
]
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.register, name = 'register'),
    path('register', views.home, name = 'register'),
    path('login', views.login, name = 'login')
]

from django.contrib import admin
from django.urls import path
from account import views

urlpatterns = [
     path('register/', views.RegistrationAPIView.as_view(), name='register' ),
     path('active/<uid64>/<token>/', views.activate, name = 'activate'),
     path('login/', views.LoginAPIView.as_view(), name='login' ),
     path('logout/', views.LogoutAPIView.as_view(), name='logout' ),
     path('me/', views.MeAPI.as_view(), name='MeAPI' ),
]

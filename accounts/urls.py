from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='account'),
    path('profile/',views.user_profile,name='profile'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
]
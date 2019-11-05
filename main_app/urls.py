from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update')
]

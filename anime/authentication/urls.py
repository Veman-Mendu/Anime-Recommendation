from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('main', views.main, name='main'),
    path('random',views.random, name='random'),
    path('recommendation', views.recommendation, name='recommendation'),
]
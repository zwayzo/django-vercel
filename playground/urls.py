from django.urls import path
from . import views
from django.conf.urls import handler404
from playground import views as playground_views

urlpatterns = [
    path('welcome/', views.welcome, name="welcome"),
    path('', views.playground, name="playground"),
]



 
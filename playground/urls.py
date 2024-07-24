from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name="welcome"),
    path('spanish/', views.spanish),
    path('', views.playground, name="playground"),
    path('<str:pk>/', views.playground, name="playground"),
    path('test/', views.test),
    # path('1/', views.test),
]

 
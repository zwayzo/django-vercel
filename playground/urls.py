from django.urls import path
from . import views
from django.conf.urls import handler404
from playground import views as playground_views

urlpatterns = [
    path('welcome/', views.welcome, name="welcome"),
    path('', views.playground, name="playground"),
    # path('<str:pk>/', views.playground, name="playground"),
    path('test/', views.test),
    # path('sign_in/', views.sign_in, name='sign_in'),
    # path('sign_up/', views.sign_up, name='sign_up')
    # path('1/', views.test),
]



 
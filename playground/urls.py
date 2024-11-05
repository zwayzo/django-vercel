from django.urls import path, include
from . import views
from django.conf.urls import handler404
from playground import views as playground_views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('items/', include('item.urls')),
    
]



 
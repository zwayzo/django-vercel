from django.urls import path, include
from . import views
from django.conf.urls import handler404
from playground import views as playground_views
from . import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('items/', include('item.urls')),
    # path('auth/login/', views.login, name='login'),
    # path('auth/callback/', views.callback, name='callback'),
    
    
]



 
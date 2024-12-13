from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('', views.detail, name='detail'),
    path('items_list/', views.Item_list),
    path('items_detail/<int:id>/', views.Item_detail),

]

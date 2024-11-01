from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from playground import views as playground_view
from django.conf.urls.static import static
from django.conf import settings
from playground.views import index, base, contact
from playground import views as pviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin', admin.site.urls),
    path('', playground_view.welcome, name='playground'),
    path('playground/', include('playground.urls')),
    path('_debug_/', include(debug_toolbar.urls)),
    path('sign_in/', pviews.sign_in, name='sign_in'),
    path('sign_up/', pviews.sign_up, name='sign_up'),
    path('contact/', contact, name='contact'),
    
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from playground import views as playground_view
from django.conf.urls.static import static
from django.conf import settings
from playground.views import index, base, contact
from playground import views as pviews
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('admin', admin.site.urls),
    path('', playground_view.index, name='playground'),
    path('playground/', include('playground.urls')),
    path('_debug_/', include(debug_toolbar.urls)),
    path('sign_in/', pviews.sign_in, name='sign_in'),
    path('sign_up/', pviews.sign_up, name='sign_up'),
    path('sign_out/', pviews.sign_out, name='sign_out'),
    path('profile/', pviews.profile, name='profile'),
    path('contact/', contact, name='contact'),
    path('auth/login/', pviews.loginView, name='login'),
    path('auth/callback/', pviews.callback, name='callback'),

    
    path('login/oauth/authorize', pviews.G_loginView, name='login'),
    path('callback/', pviews.G_callback, name='callback'),
    
    # path('sign_in/', view=auth_views.LoginView.as_view(template_name='playground/sign_in.html'), name='sign_in'),
    # path('logout/', auth_views.LogoutView.as_view(), name='sign_out'),    
    
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

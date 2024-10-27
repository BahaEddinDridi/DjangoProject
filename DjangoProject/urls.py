"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from . import views

  # include is imported here

urlpatterns = [
    path('admin/', admin.site.urls),
     path('login/', LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('fitness.urls',)),
    path('goals/', include('goals.urls')),
    path('hormones/',include('hormones.urls')),
    
    path('recipes/', include('recipes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

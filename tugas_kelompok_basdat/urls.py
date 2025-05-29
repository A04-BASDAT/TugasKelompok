"""
URL configuration for tugas_kelompok_basdat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('animals/', include('animals.urls')),
    path('habitats/', include('habitats.urls')),
    path('medical/', include('medical.urls')),
    path('feeding/', include('feeding.urls')),
    path('attractions/', include('attractions.urls')),
    path('tickets/', include('tickets.urls')),
    path('adoptions/', include('adoptions.urls')),
    path('administrative-staff/', include('administrative_staff.urls')),
    path('adopter/', include('adopter.urls')),
    path('feeding/', include(('feeding.urls', 'feeding'), namespace='feeding')),
    path('medical/', include(('medical.urls', 'medical'), namespace='medical')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


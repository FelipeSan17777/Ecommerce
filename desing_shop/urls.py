"""
URL configuration for desing_shop project.

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
from django.urls import path
from ropaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio),
    path('carrito/',views.carrito),
    path('iniciar/',views.iniciar),
    path('pantalones/',views.pantalones),
    path('chaqueta/',views.chaqueta),
    path('poleras/',views.poleras),
    path('polerones/',views.polerones),
    path('abrigos/',views.abrigos),
]

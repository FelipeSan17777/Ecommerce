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
    path('adminn/', views.admin),
    path('', views.inicio, name='inicio'),
    path('carrito/', views.carrito, name='carrito'),
    path('iniciar/', views.iniciar, name='iniciar'),
    path('pantalones/', views.pantalones, name='pantalones'),
    path('registrar/', views.registro),
    path('pantalones/<int:id>/', views.detalle_pantalon, name='detalle_pantalon'), 
    path('cerrar/', views.cerrar_sesion, name='cerrar_sesion'),
    path('agregar-al-carrito/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('usuarios/', views.ver_usuarios, name='ver_usuarios'),
]

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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminn/', views.admin),
    path('', views.inicio, name='inicio'),
    path('carrito/', views.carrito, name='carrito'),
    path('iniciar/', views.iniciar, name='iniciar'),
    path('pantalones/', views.productos_por_categoria, name='pantalones'),
    path('registrar/', views.registro),
    path('cerrar/', views.cerrar_sesion, name='cerrar_sesion'),
    path('agregar-al-carrito/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar-del-carrito/<str:id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('pantalones/agregar/', views.agregar_ropa, name='agregar_ropa'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('pantalon/<int:id>/', views.detalle_pantalon, name='detalle_pantalon'),
    path('realizar-pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('productos/', views.ver_productos, name='ver_productos'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('categorias/', views.ver_categorias, name='ver_categorias'),              
    path('categoria/<int:id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('datos-cliente/', views.datos_cliente, name='datos_cliente'),
    path('pagar/', views.pagar_con_stripe, name='pagar_stripe'),
    path('pago/exito/', views.pago_exito, name='pago_exito'),
    path('pago/cancelado/', views.pago_cancelado, name='pago_cancelado'),
    path('acerca-de-nosotros/', views.acerca_de_nosotros, name='acerca_de_nosotros'),
    path('servicios/', views.servicios, name='servicios'),
    path('politica-de-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('preguntas-frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('pedido/<int:pedido_id>/entregado/', views.marcar_entregado, name='marcar_entregado'),
    path('mis-pedidos/', views.ver_mis_pedidos, name='mis_pedidos'),
    path('envios-valdivia/', views.envios_valdivia, name='envios_valdivia'),
    path('proceso-venta/', views.proceso_venta, name='proceso_venta'),

        

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

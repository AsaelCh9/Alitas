from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('registro/', views.registro, name='registro'),

    path(
        'agregar/<int:producto_id>/',
        views.agregar_carrito,
        name='agregar_carrito'
    ),

    path('carrito/', views.ver_carrito, name='carrito'),

    path(
        'quitar/<int:producto_id>/',
        views.quitar_carrito,
        name='quitar_carrito'
    ),

    path('checkout/', views.finalizar_pedido, name='checkout'),

    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
]
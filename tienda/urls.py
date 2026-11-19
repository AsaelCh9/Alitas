from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('nuevo/', views.agregar_producto, name='agregar_producto'), 
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
]
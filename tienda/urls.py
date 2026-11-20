from django.urls import path
from . import views

urlpatterns = [
path('', views.inicio, name='inicio'),
path('registro/', views.registro_usuario, name='registro'),
path('login/', views.login_usuario, name='login'),
path('logout/', views.logout_usuario, name='logout'),
path('nuevo/', views.agregar_producto, name='agregar_producto'),
path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
path('carrito/', views.ver_carrito, name='ver_carrito'),
path('confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
]
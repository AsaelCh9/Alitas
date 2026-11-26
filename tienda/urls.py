from django.urls import path
from . import views

urlpatterns = [
    # Tienda y autenticación
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('confirmar/', views.confirmar_pedido, name='confirmar_pedido'),

    # Panel administrativo
    path('panel/', views.dashboard, name='dashboard'),

    # CRUD Productos
    path('panel/productos/', views.lista_productos, name='lista_productos'),
    path('panel/productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('panel/productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('panel/productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # CRUD Categorías
    path('panel/categorias/', views.lista_categorias, name='lista_categorias'),
    path('panel/categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('panel/categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('panel/categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),

    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
]
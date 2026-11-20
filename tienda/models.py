from django.db import models
from django.contrib.auth.models import User

# Entidad 1: Categorías de productos (PK: id automático)
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150, blank=True)
    
    def __str__(self):
        return self.nombre
        
# Entidad 2: Productos (FK hacia Categoria)
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=250)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
        
# Entidad 3: Pedidos realizados (FK hacia User y Producto)
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.username}"
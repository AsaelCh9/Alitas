from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('alitas', 'Alitas'),
        ('boneless', 'Boneless'),
        ('complementos', 'Complementos'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=250)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='alitas')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio})"
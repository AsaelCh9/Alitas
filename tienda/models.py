from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):

    CATEGORIAS = {
        ('alitas', 'Alitas'),
        ('combos', 'Combos'),
        ('complementos', 'Complementos'),
        ('bebidas', 'bebidas'),
    }

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS
     )

    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    precio_oferta = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True

    )

    imagen = models.URLField(blank=True)

    destacado = models.BooleanField(default=False)
    disponible = models.BooleanField(default=True)

    def precio_final(self):
        if self.precio_oferta is not None:
            if self.precio_oferta < self.precio:
                return self.precio_oferta
            return self.precio

        def __str__(self):
            return self.nombre

        class Cliente(models.Model):

            usuario = models.OneToOneField(
                 User,
                   on_delete=models.CASCADE,
            )

            telefono = models.CharField(max_length=20)
from django.contrib import admin
from .models import Categoria, Producto, Pedido

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)

admin.site.register(Categoria)
admin.site.register(Pedido)
from django import forms
from .models import Producto, Categoria

ESTILO_INPUT = 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm focus:outline-none focus:border-stone-900'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen', 'disponible']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': ESTILO_INPUT, 'placeholder': 'Ej. 12 Alitas Búfalo'}),
            'descripcion': forms.Textarea(attrs={'class': ESTILO_INPUT, 'rows': 3, 'placeholder': 'Descripción del platillo...'}),
            'precio': forms.NumberInput(attrs={'class': ESTILO_INPUT, 'step': '0.01', 'min': '1'}),
            'categoria': forms.Select(attrs={'class': f'{ESTILO_INPUT} bg-white'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'w-full text-xs text-stone-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:bg-stone-100 file:text-stone-900'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'w-4 h-4 accent-orange-600 rounded'}),
        }

    # Validación en el servidor
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a $0.00.")
        return precio

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': ESTILO_INPUT, 'placeholder': 'Ej. Alitas, Boneless, Bebidas'}),
            'descripcion': forms.TextInput(attrs={'class': ESTILO_INPUT, 'placeholder': 'Breve descripción de la categoría'}),
        }
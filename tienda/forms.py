from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm focus:outline-none focus:border-stone-900',
                'placeholder': 'Ej. 12 Alitas Mango Habanero'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm focus:outline-none focus:border-stone-900',
                'rows': 3,
                'placeholder': 'Describe el sabor, aderezo o guarnición...'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm focus:outline-none focus:border-stone-900',
                'placeholder': '180.00'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-stone-200 text-sm bg-white focus:outline-none focus:border-stone-900'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'w-full text-xs text-stone-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-medium file:bg-stone-100 file:text-stone-900 hover:file:bg-stone-200 cursor-pointer'
            }),
        }
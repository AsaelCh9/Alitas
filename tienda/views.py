from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm 

def inicio(request):
    productos = Producto.objects.filter(disponible=True)
    carrito = request.session.get('carrito', {})
    total_items = sum(carrito.values())
   
    return render(request, 'tienda/index.html', {
        'productos': productos,
        'total_items': total_items
    })

def agregar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)
   
    if producto_id_str in carrito:
        carrito[producto_id_str] += 1
    else:
        carrito[producto_id_str] = 1
       
    request.session['carrito'] = carrito
    return redirect('inicio')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total_pagar = 0

    for prod_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=int(prod_id))
        subtotal = producto.precio * cantidad
        total_pagar += subtotal
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })

    return render(request, 'tienda/carrito.html', {
        'items': items,
        'total_pagar': total_pagar,
        'total_items': sum(carrito.values())
    })

def limpiar_carrito(request):
    request.session['carrito'] = {}
    return redirect('ver_carrito')

def agregar_producto(request):
    if request.method == 'POST':
        # request.FILES es obligatorio para recibir la imagen
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ProductoForm()
       
    carrito = request.session.get('carrito', {})
    return render(request, 'tienda/agregar_producto.html', {
        'form': form,
        'total_items': sum(carrito.values())
    })
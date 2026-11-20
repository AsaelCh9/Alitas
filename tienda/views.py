from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria, Pedido
from .forms import ProductoForm

# --- AUTENTICACIÓN (SPRINT 2) ---
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'tienda/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'tienda/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('login')
# --- VISTAS DEL SISTEMA ---
def inicio(request):
    productos = Producto.objects.filter(disponible=True)
    carrito = request.session.get('carrito', {})
    return render(request, 'tienda/index.html', {
        'productos': productos,
        'total_items': sum(carrito.values())
        })

# Sección protegida: requiere iniciar sesión
@login_required(login_url='login')
def agregar_producto(request):
    if request.method == 'POST':
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('inicio')
    else:
                form = ProductoForm()
    return render(request, 'tienda/agregar_producto.html', {'form': form})
                
@login_required(login_url='login')
def agregar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    prod_str = str(producto_id)
    carrito[prod_str] = carrito.get(prod_str, 0) + 1
    request.session['carrito'] = carrito
    return redirect('inicio')
                    
@login_required(login_url='login')
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total_pagar = 0
    for prod_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=int(prod_id))
        subtotal = producto.precio * cantidad
        total_pagar += subtotal
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
        return render(request, 'tienda/carrito.html', {
            'items': items,
            'total_pagar': total_pagar,
            'total_items': sum(carrito.values())
            })
                                
@login_required(login_url='login')
def confirmar_pedido(request):
    carrito = request.session.get('carrito', {})
    for prod_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=int(prod_id))
        Pedido.objects.create(usuario=request.user, producto=producto, cantidad=cantidad)
    request.session['carrito'] = {}
    return redirect('inicio')
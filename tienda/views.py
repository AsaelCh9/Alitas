from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from .models import Producto, Categoria, Pedido
from .forms import ProductoForm, CategoriaForm

# Función verificadora de rol Administrador (valida en servidor)
def es_administrador(user):
    return user.is_authenticated and user.is_staff

# --- AUTENTICACIÓN ---
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"¡Bienvenido, {usuario.username}! Tu cuenta ha sido creada.")
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
            messages.success(request, f"Sesión iniciada como {usuario.username}.")
            if usuario.is_staff:
                return redirect('dashboard')
            return redirect('inicio')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'tienda/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')

# --- TIENDA (PÚBLICO / CLIENTES) ---
def inicio(request):
    productos = Producto.objects.filter(disponible=True)
    carrito = request.session.get('carrito', {})
    return render(request, 'tienda/index.html', {
        'productos': productos,
        'total_items': sum(carrito.values())
    })

@login_required(login_url='login')
def agregar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    prod_str = str(producto_id)
    carrito[prod_str] = carrito.get(prod_str, 0) + 1
    request.session['carrito'] = carrito
    messages.success(request, "Platillo agregado a tu orden.")
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
def limpiar_carrito(request):
    request.session['carrito'] = {}
    messages.info(request, "Tu orden ha sido vaciada.")
    return redirect('ver_carrito')

@login_required(login_url='login')
def confirmar_pedido(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('inicio')
    for prod_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=int(prod_id))
        Pedido.objects.create(usuario=request.user, producto=producto, cantidad=cantidad)
    request.session['carrito'] = {}
    messages.success(request, "¡Pedido confirmado! Tu orden ya se registró en el sistema.")
    return redirect('inicio')

# --- DASHBOARD ADMINISTRATIVO (SOLO ROL ADMIN) ---
@user_passes_test(es_administrador, login_url='inicio')
def dashboard(request):
    contexto = {
        'total_productos': Producto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_pedidos': Pedido.objects.count(),
        'total_usuarios': User.objects.count(),
        'ultimos_pedidos': Pedido.objects.select_related('usuario', 'producto').order_by('-fecha')[:5],
    }
    return render(request, 'tienda/dashboard.html', contexto)

# --- CRUD DE PRODUCTOS (SOLO ROL ADMIN) ---
@user_passes_test(es_administrador, login_url='inicio')
def lista_productos(request):
    productos = Producto.objects.select_related('categoria').all()
    return render(request, 'tienda/crud_productos.html', {'productos': productos})

@user_passes_test(es_administrador, login_url='inicio')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto registrado correctamente.")
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'tienda/form_producto.html', {'form': form, 'titulo': 'Nuevo Producto'})

@user_passes_test(es_administrador, login_url='inicio')
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f"El producto '{producto.nombre}' fue actualizado.")
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/form_producto.html', {'form': form, 'titulo': f'Editar: {producto.nombre}'})

@user_passes_test(es_administrador, login_url='inicio')
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"Producto '{nombre}' eliminado permanentemente.")
        return redirect('lista_productos')
    return render(request, 'tienda/confirmar_eliminar.html', {'objeto': producto, 'tipo': 'Producto', 'url_cancelar': 'lista_productos'})

# --- CRUD DE CATEGORÍAS (SOLO ROL ADMIN) ---
@user_passes_test(es_administrador, login_url='inicio')
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'tienda/crud_categorias.html', {'categorias': categorias})

@user_passes_test(es_administrador, login_url='inicio')
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente.")
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'tienda/form_categoria.html', {'form': form, 'titulo': 'Nueva Categoría'})

@user_passes_test(es_administrador, login_url='inicio')
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada correctamente.")
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'tienda/form_categoria.html', {'form': form, 'titulo': f'Editar: {categoria.nombre}'})

@user_passes_test(es_administrador, login_url='inicio')
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect('lista_categorias')
    return render(request, 'tienda/confirmar_eliminar.html', {'objeto': categoria, 'tipo': 'Categoría', 'url_cancelar': 'lista_categorias'})
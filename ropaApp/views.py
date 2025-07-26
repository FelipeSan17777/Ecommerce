from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pantalones, Usuario, Categoria , DetallePedido,Pedido
from desing_shop import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def inicio(request):
    categorias = Categoria.objects.all()[:2]  
    productos_cat1 = Pantalones.objects.filter(categoria=categorias[0])[:3] if categorias.count() > 0 else []
    productos_cat2 = Pantalones.objects.filter(categoria=categorias[1])[:3] if categorias.count() > 1 else []

    context = {
        'categoria1': categorias[0] if categorias.count() > 0 else None,
        'productos_cat1': productos_cat1,
        'categoria2': categorias[1] if categorias.count() > 1 else None,
        'productos_cat2': productos_cat2,
    }
    return render(request, 'inicio.html', context)

def admin(request):
    return render(request, "administrador.html")

def cerrar_sesion(request):
    request.session.flush()
    return redirect('inicio')

def acerca_de_nosotros(request):
    return render(request, 'acerca_de_nosotros.html')

def servicios(request):
    return render(request, 'servicios.html')

def politica_privacidad(request):
    return render(request, 'politica_privacidad.html')

def preguntas_frecuentes(request):
    return render(request, 'preguntas_frecuentes.html')



def iniciar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(nombre_usuario=username)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
            return render(request, "inicio_sesion.html")

        if usuario.contraseña != password:
            messages.error(request, "Contraseña incorrecta")
            return render(request, "inicio_sesion.html")

        # Guardar datos en sesión
        request.session['usuario_id'] = usuario.id  
        request.session['username'] = usuario.nombre_usuario
        request.session['tipo_usuario'] = usuario.tipo_usuario

        return redirect('inicio') 

    return render(request, "inicio_sesion.html")

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'registrar.html')

        if Usuario.objects.filter(nombre_usuario=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso")
            return render(request, 'registrar.html')

        if Usuario.objects.filter(correo=email).exists():
            messages.error(request, "El correo electrónico ya está en uso")
            return render(request, 'registrar.html')

        nuevo_usuario = Usuario(
            nombre_usuario=username,
            contraseña=password1,
            correo=email,
            telefono=telefono,
            tipo_usuario='user'
        )
        nuevo_usuario.save()
        messages.success(request, "Su registro fue exitoso")
        return render(request, 'inicio_sesion.html')

    return render(request, 'registrar.html')

def ver_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'ver_usuarios.html', {'usuarios': usuarios})



def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            Categoria.objects.create(nombre=nombre)
            messages.success(request, "Categoría creada correctamente.")
            return redirect('crear_categoria')  

    return render(request, 'agregar_categoria.html')
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        if 'guardar' in request.POST:
            nuevo_nombre = request.POST.get('nombre')
            if nuevo_nombre:
                categoria.nombre = nuevo_nombre
                categoria.save()
                messages.success(request, "Categoría actualizada correctamente.")
                return redirect('ver_categorias') 

        elif 'eliminar' in request.POST:
            categoria.delete()
  
            return redirect('ver_categorias')  

    return render(request, 'editar_categoria.html', {'categoria': categoria})

def categorias_disponibles(request):
    categorias = Categoria.objects.all()
    return {
        'categorias': categorias
    }
def ver_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'ver_categorias.html', {'categorias': categorias})
    
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Pantalones.objects.filter(categoria=categoria)
    return render(request, 'pantalones.html', {
        'categoria': categoria,
        'pantalones': productos 
    })

def detalle_pantalon(request, id):
    pantalon = get_object_or_404(Pantalones, id=id)
    tallas_cantidades = [
        ('XS', pantalon.cantidad_xs),
        ('S', pantalon.cantidad_s),
        ('M', pantalon.cantidad_m),
        ('L', pantalon.cantidad_l),
        ('XL', pantalon.cantidad_xl),
    ]
    return render(request, 'detalle.html', {
        'pantalon': pantalon,
        'tallas_cantidades': tallas_cantidades,
    })

def agregar_ropa(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = int(request.POST.get('precio'))
        imagen = request.FILES.get('imagen')
        categoria_id = request.POST.get('categoria')  

        cantidad_xs = request.POST.get('cantidad_xs', 0)
        cantidad_s = request.POST.get('cantidad_s', 0)
        cantidad_m = request.POST.get('cantidad_m', 0)
        cantidad_l = request.POST.get('cantidad_l', 0)
        cantidad_xl = request.POST.get('cantidad_xl', 0)

        categoria = get_object_or_404(Categoria, id=categoria_id)  

        nuevo_pantalon = Pantalones(
            nombre=nombre,
            precio=precio,
            imagen=imagen,
            categoria=categoria,  
            cantidad_xs=cantidad_xs,
            cantidad_s=cantidad_s,
            cantidad_m=cantidad_m,
            cantidad_l=cantidad_l,
            cantidad_xl=cantidad_xl
        )
        nuevo_pantalon.save()
        return redirect('agregar_ropa')

    categorias = Categoria.objects.all() 
    return render(request, 'agregar_ropa.html', {'categorias': categorias})


def carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0

    for item in carrito.values():
        subtotal = item['precio'] * item['cantidad']
        item['subtotal'] = round(subtotal, 2)
        total += subtotal

    context = {
        'carrito': carrito,
        'total': round(total, 2)
    }
    return render(request, "carrito.html", context)


def agregar_al_carrito(request, id):
    pantalon = get_object_or_404(Pantalones, id=id)
    
    talla = request.POST.get('talla')
    cantidad_input = request.POST.get('cantidad', '1')

    try:
        cantidad = int(cantidad_input)
        if cantidad < 1:
            raise ValueError
    except ValueError:
        messages.error(request, "La cantidad debe ser un número entero mayor a 0.", extra_tags='carrito')
        return redirect('detalle_pantalon', id=id)

    
    cantidad_disponible = 0
    if talla == 'XS':
        cantidad_disponible = pantalon.cantidad_xs
    elif talla == 'S':
        cantidad_disponible = pantalon.cantidad_s
    elif talla == 'M':
        cantidad_disponible = pantalon.cantidad_m
    elif talla == 'L':
        cantidad_disponible = pantalon.cantidad_l
    elif talla == 'XL':
        cantidad_disponible = pantalon.cantidad_xl
    else:
        messages.error(request, "Talla inválida.", extra_tags='carrito')
        return redirect('detalle_pantalon', id=id)


    carrito = request.session.get('carrito', {})
    key = f"{id}_{talla}"
    cantidad_actual_en_carrito = carrito.get(key, {}).get('cantidad', 0)

    if cantidad + cantidad_actual_en_carrito > cantidad_disponible:
        disponible = cantidad_disponible - cantidad_actual_en_carrito
        messages.error(request, f"No hay suficiente stock para la talla {talla}. Disponible: {disponible}", extra_tags='carrito')
        return redirect('detalle_pantalon', id=id)


    if key in carrito:
        carrito[key]['cantidad'] += cantidad
    else:
        carrito[key] = {
            'nombre': pantalon.nombre,
            'precio': int(pantalon.precio),
            'cantidad': cantidad,
            'talla': talla,
            'imagen': str(pantalon.imagen),
        }

    request.session['carrito'] = carrito
    messages.success(request, f"{cantidad} x {pantalon.nombre} (Talla {talla}) agregado al carrito.", extra_tags='carrito')
    return redirect('carrito')

def quitar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    id_str = str(id)

    if id_str in carrito:
        if carrito[id_str]['cantidad'] > 1:
            carrito[id_str]['cantidad'] -= 1
            carrito[id_str]['subtotal'] = carrito[id_str]['cantidad'] * carrito[id_str]['precio']
        else:
            del carrito[id_str]

        request.session['carrito'] = carrito

    return redirect('carrito')

def realizar_pedido(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        carrito = request.session.get('carrito', {})

        if not carrito:
            messages.error(request, "El carrito está vacío.")
            return redirect('carrito')

  
        total = sum(item['precio'] * item['cantidad'] for item in carrito.values())


        pedido = Pedido.objects.create(
            nombre_cliente=nombre,
            direccion_entrega=direccion,
            total=total
        )


        for key, item in carrito.items():
            producto_id = key.split('_')[0]
            talla = item.get('talla')
            cantidad = item.get('cantidad')
            precio_unitario = item.get('precio')
            subtotal = cantidad * precio_unitario

            producto = get_object_or_404(Pantalones, id=producto_id)

            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                talla=talla,
                subtotal=subtotal
            )


        request.session['carrito'] = {}
        messages.success(request, "¡Pedido realizado con éxito!")

        return redirect('inicio')  

    return render(request, 'realizar_pedido.html')

def pagar_con_stripe(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('carrito')

    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'clp',
                        'product_data': {
                            'name': 'Compra en Design_shop.cl',
                        },
                        'unit_amount': int(total), 
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/pago/exito/'),
            cancel_url=request.build_absolute_uri('/pago/cancelado/'),
            metadata={
                'carrito': str(carrito),
            }
        )
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, "Error al generar sesión de pago: " + str(e))
        return redirect('carrito')

def envios_valdivia(request):
    return render(request, 'envios_valdivia.html')

def proceso_venta(request):
    return render(request, 'proceso_venta.html')
    
def pago_exito(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('carrito')
    usuario = Usuario.objects.filter(nombre_usuario=request.session.get('username')).first()
    nombre = request.session.get('nombre_cliente', 'Anónimo')
    direccion = request.session.get('direccion_entrega', 'Sin dirección')

    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    

    pedido = Pedido.objects.create(
        usuario=usuario,
        nombre_cliente=nombre,
        direccion_entrega=direccion,
        total=total
    )


    for key, item in carrito.items():
        producto_id = key.split('_')[0]
        talla = item.get('talla')
        cantidad = item.get('cantidad')
        precio_unitario = item.get('precio')
        subtotal = cantidad * precio_unitario
        producto = get_object_or_404(Pantalones, id=producto_id)


        if talla == 'XS':
            producto.cantidad_xs = max(producto.cantidad_xs - cantidad, 0)
        elif talla == 'S':
            producto.cantidad_s = max(producto.cantidad_s - cantidad, 0)
        elif talla == 'M':
            producto.cantidad_m = max(producto.cantidad_m - cantidad, 0)
        elif talla == 'L':
            producto.cantidad_l = max(producto.cantidad_l - cantidad, 0)
        elif talla == 'XL':
            producto.cantidad_xl = max(producto.cantidad_xl - cantidad, 0)

        producto.save()


        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            talla=talla,
            subtotal=subtotal
        )


    request.session['carrito'] = {}

    messages.success(request, "¡Pago y pedido exitoso!")
    return render(request, 'pago_exito.html')


def pago_cancelado(request):
    messages.warning(request, "Pago cancelado.")
    return render(request, 'pago_cancelado.html')


def datos_cliente(request):
    if request.method == 'POST':
        request.session['nombre_cliente'] = request.POST.get('nombre')
        request.session['direccion_entrega'] = request.POST.get('direccion')
        return redirect('pagar_stripe')
    return render(request, 'datos_cliente.html')

def ver_pedidos(request):
    pedidos = Pedido.objects.prefetch_related('detalles').all().order_by('-fecha')
    return render(request, 'ver_pedidos.html', {'pedidos': pedidos})

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles
    })
    
def ver_productos(request):
    productos = Pantalones.objects.filter(
        detallepedido__estado_entrega=False
    ).select_related('categoria').distinct()
    return render(request, 'ver_productos.html', {'productos': productos})
def editar_producto(request, id):
    producto = get_object_or_404(Pantalones, id=id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        if 'guardar' in request.POST:
            producto.nombre = request.POST.get('nombre')
            producto.precio = request.POST.get('precio')
            producto.cantidad_xs = request.POST.get('cantidad_xs', 0)
            producto.cantidad_s = request.POST.get('cantidad_s', 0)
            producto.cantidad_m = request.POST.get('cantidad_m', 0)
            producto.cantidad_l = request.POST.get('cantidad_l', 0)
            producto.cantidad_xl = request.POST.get('cantidad_xl', 0)
            categoria_id = request.POST.get('categoria')

            producto.categoria = get_object_or_404(Categoria, id=categoria_id)
            producto.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('ver_productos')

        elif 'eliminar' in request.POST:
            producto.delete()
            messages.success(request, "Producto eliminado correctamente.")
            return redirect('ver_productos')

    return render(request, 'editar_producto.html', {
        'producto': producto,
        'categorias': categorias
    })
def perfil_usuario(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('iniciar')  

    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'perfil.html', {'usuario': usuario})

def marcar_entregado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.detalles.update(estado_entrega=True)
    

    return redirect('ver_pedidos')

def ver_mis_pedidos(request):
    nombre_usuario = request.session.get('username')
    if not nombre_usuario:
        return render(request, 'acceso_denegado.html', {
            'mensaje': 'Debes hacerte una cuenta e iniciar sesión para ver el estatus de tus pedidos.'
        })

    usuario = get_object_or_404(Usuario, nombre_usuario=nombre_usuario)
    pedidos = Pedido.objects.filter(usuario=usuario).order_by('-fecha')

    pedidos_con_detalles = []

    for pedido in pedidos:
        detalles = DetallePedido.objects.filter(pedido=pedido)
        for d in detalles:
            if d.estado_entrega is None:
                d.estado_entrega = True

        pedidos_con_detalles.append({
            'pedido': pedido,
            'detalles': detalles
        })

    return render(request, 'mis_pedidos.html', {
        'pedidos_con_detalles': pedidos_con_detalles,
        'nombre_usuario': nombre_usuario 
    })
 
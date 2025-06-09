from django.shortcuts import render
from .models import Pantalones,Usuario
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

def inicio(request):
    return render(request,"inicio.html")

def ver_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'ver_usuarios.html', {'usuarios': usuarios})

def carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0

    for item in carrito.values():
        subtotal = float(item['precio']) * int(item['cantidad'])
        item['subtotal'] = round(subtotal, 2)
        total += subtotal

    context = {
        'carrito': carrito,
        'total': round(total, 2)
    }
    return render(request, "carrito.html", context)

def agregar_al_carrito(request, id):
    pantalon = get_object_or_404(Pantalones, id=id)

    carrito = request.session.get('carrito', {})

    id_str = str(id)
    if id_str in carrito:
        carrito[id_str]['cantidad'] += 1
    else:
        carrito[id_str] = {
            'nombre': pantalon.nombre,
            'precio': float(pantalon.precio),
            'cantidad': 1,
            'imagen': str(pantalon.imagen),  # Asumiendo que es un string
        }

    request.session['carrito'] = carrito
    messages.success(request, f"{pantalon.nombre} agregado al carrito.")
    return redirect('carrito')

def quitar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    id_str = str(id)
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito 

    return redirect('carrito')

def cerrar_sesion(request):
    request.session.flush()  
    return redirect('inicio')

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

        request.session['username'] = usuario.nombre_usuario
        request.session['tipo_usuario'] = usuario.tipo_usuario

        return redirect('inicio')  

    return render(request, "inicio_sesion.html")


def admin(request):
    return render(request,"administrador.html")

def pantalones(request):
    p = Pantalones.objects.all()
    
    data = {
        'pantalones':p,
    }
    return render(request,'pantalones.html',data)

def detalle_pantalon(request, id):
    pantalon = get_object_or_404(Pantalones, id=id)
    return render(request, 'detalle.html', {'pantalon': pantalon})

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
        return render(request, 'registrar.html') 

    return render(request, 'registrar.html')
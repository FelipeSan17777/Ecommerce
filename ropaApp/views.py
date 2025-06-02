from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request,"inicio.html")

def carrito(request):
    return render(request,"carrito.html")

def iniciar(request):
    return render(request,"inicio_sesion.html")

def pantalones(request):
    return render(request,"pantalones.html")


def chaqueta(request):
    return render(request,"chaqueta.html")

def poleras(request):
    return render(request,"polera.html")

def polerones(request):
    return render(request,"polerones.html")

def abrigos(request):
    return render(request,"abrigos.html")
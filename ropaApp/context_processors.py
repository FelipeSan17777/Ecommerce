from .models import Categoria

def categorias_disponibles(request):
    categorias = Categoria.objects.all()
    return {'categorias': categorias}
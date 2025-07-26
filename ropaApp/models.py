from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Pantalones(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='pantalones/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    cantidad_xs = models.IntegerField(default=0)
    cantidad_s = models.IntegerField(default=0)
    cantidad_m = models.IntegerField(default=0)
    cantidad_l = models.IntegerField(default=0)
    cantidad_xl = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=50, null=False)
    contraseña = models.CharField(max_length=40, null=False)
    correo = models.CharField(max_length=200, null=False)
    telefono = models.CharField(max_length=40, null=False)
    tipo_usuario = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.nombre_usuario


class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    nombre_cliente = models.CharField(max_length=100)
    direccion_entrega = models.CharField(max_length=255)
    total = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Pantalones, on_delete=models.CASCADE)
    talla = models.CharField(max_length=5)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    estado_entrega = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Talla {self.talla})"

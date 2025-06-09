from django.db import models

# Create your models here.
class Pantalones(models.Model):
    TALLAS = [
        ('XS', 'Extra Pequeña'),
        ('S', 'Pequeña'),
        ('M', 'Mediana'),
        ('L', 'Grande'),
        ('XL', 'Extra Grande'),
    ]
    nombre = models.CharField(max_length=50, null=False)
    talla = models.CharField(max_length=2, choices=TALLAS, null=False)
    precio = models.IntegerField(default=0)
    imagen = models.CharField(max_length=200)
    
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=50,null=False)
    contraseña = models.CharField(max_length=40, null=False)
    correo = models.CharField(max_length=200,null=False)
    telefono = models.CharField(max_length=40,null=False)
    tipo_usuario = models.CharField(max_length=10,null=True)


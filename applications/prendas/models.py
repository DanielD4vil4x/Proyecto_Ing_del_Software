from django.db import models

class Prenda(models.Model):
    nombre_prenda = models.CharField(max_length=100)
    color_prenda = models.CharField(max_length=50)
    talla_prenda = models.CharField(max_length=10)
    categoria_prenda = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='prendas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_prenda} - {self.talla_prenda}"
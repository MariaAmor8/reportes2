from django.db import models

# Create your models here.

class Reporte(models.Model):
    codigo = models.IntegerField(default=None)
    estudiante = models.IntegerField(default=None)
    fechaEmision = models.DateTimeField(auto_now_add=True)
    emisor = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s %s' % (self.estudiante.nombre, self.fechaEmision)
    

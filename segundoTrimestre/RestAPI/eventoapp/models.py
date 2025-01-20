from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('organizador', 'Organizador'),
        ('participante', 'Participante'),
    ]
    biografia = models.TextField(blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField()
    capacidad = models.PositiveIntegerField()
    imagen_url = models.URLField(blank=True, null=True)
    pelicula = models.CharField(max_length=200)
    organizador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="eventos")

    def __str__(self):
        return self.titulo


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reservas")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="reservas", null = True, blank= True)
    entradas = models.PositiveIntegerField( null = True, blank= True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Reserva de {self.usuario} para {self.evento}"


class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="comentarios")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="comentarios", null = True, blank= True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario} en {self.evento}"
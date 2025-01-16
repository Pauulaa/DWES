from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo de Usuario Personalizado
class UsuarioPersonalizado(AbstractUser):
    biografia = models.TextField(blank=True, null=True)
    ROL_CHOICES = [
        ('organizador', 'Organizador'),
        ('participante', 'Participante'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='participante')

    def __str__(self):
        return self.username

# Modelo de Libro
class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    fecha_publicacion = models.DateField()
    categoria = models.CharField(max_length=255)
    cantidad_disponible = models.IntegerField()
    imagen_url = models.URLField()

    def __str__(self):
        return self.titulo

# Modelo de Comentario
class Comentario(models.Model):
    texto = models.TextField()
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.libro.titulo}"

# Modelo de Reserva
class Reserva(models.Model):
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.libro.titulo} - {self.estado}"



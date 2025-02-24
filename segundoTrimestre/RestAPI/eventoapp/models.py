# Importamos AbstractUser para extender el modelo de usuario de Django
from django.contrib.auth.models import AbstractUser  
# Importamos models para definir los modelos de base de datos
from django.db import models  

# Definimos un modelo de usuario personalizado que hereda de AbstractUser
class Usuario(AbstractUser):  
    # Opciones de roles que puede tener un usuario
    ROL_CHOICES = [
        ('organizador', 'Organizador'),  # Un usuario que crea eventos
        ('participante', 'Participante'),  # Un usuario que asiste a eventos
    ]

    # Campo de texto opcional donde el usuario puede escribir su biografía
    biografia = models.TextField(blank=True, null=True)  

    # Campo que almacena el rol del usuario con las opciones definidas en ROL_CHOICES
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)  

    # Define cómo se representará el usuario en textos
    def __str__(self):  
        return self.username  # Retorna el nombre de usuario


# Definimos un modelo para los eventos
class Evento(models.Model):  
    # Título del evento, hasta 200 caracteres
    titulo = models.CharField(max_length=200)  

    # Descripción larga del evento
    descripcion = models.TextField()  

    # Fecha y hora en que se realizará el evento
    fecha_hora = models.DateTimeField()  

    # Número máximo de asistentes permitidos
    capacidad = models.PositiveIntegerField()  

    # URL opcional de una imagen del evento
    imagen_url = models.URLField(blank=True, null=True)  

    # Nombre de la película que se proyectará en el evento
    pelicula = models.CharField(max_length=200)  

    # Relación con el usuario que organiza el evento
    # Si el organizador se elimina, se eliminan sus eventos
    organizador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="eventos")  

    # Define cómo se representará el evento en textos
    def __str__(self):  
        return self.titulo  # Retorna el título del evento


# Definimos un modelo para las reservas de eventos
class Reserva(models.Model):  
    # Opciones de estado de la reserva
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),  
        ('confirmada', 'Confirmada'),  
        ('cancelada', 'Cancelada'),  
    ]

    # Relación con el usuario que realiza la reserva
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reservas")  

    # Relación con el evento reservado (puede ser opcional)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="reservas", null=True, blank=True)  

    # Cantidad de entradas reservadas (puede ser opcional)
    entradas = models.PositiveIntegerField(null=True, blank=True)  

    # Estado de la reserva con opciones predefinidas, por defecto "pendiente"
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')  

    # Define cómo se representará la reserva en textos
    def __str__(self):  
        return f"Reserva de {self.usuario} para {self.evento}"  # Muestra usuario y evento reservado


# Definimos un modelo para los comentarios en eventos
class Comentario(models.Model):  
    # Texto del comentario (puede ser opcional)
    texto = models.TextField(blank=True, null=True)  

    # Relación con el usuario que escribió el comentario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="comentarios")  

    # Relación con el evento sobre el que se comenta (opcional)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="comentarios", null=True, blank=True)  

    # Fecha y hora en que se creó el comentario, se guarda automáticamente
    fecha_creacion = models.DateTimeField(auto_now_add=True)  

    # Define cómo se representará el comentario en textos
    def __str__(self):  
        return f"Comentario de {self.usuario} para {self.evento}"  # Muestra usuario y evento comentado


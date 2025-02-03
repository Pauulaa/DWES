
from django.contrib import admin
from .models import Usuario, Evento, Reserva, Comentario

# Personalización del administrador para el modelo Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'biografia')  # Mostrar estas columnas en la lista
    search_fields = ('username', 'email')  # Buscar por nombre de usuario y correo
    list_filter = ('rol',)  # Filtrar por rol

admin.site.register(Usuario, UsuarioAdmin)

# Personalización del administrador para el modelo Evento
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_hora', 'capacidad', 'organizador')  # Mostrar estas columnas en la lista
    search_fields = ('titulo', 'descripcion')  # Buscar por título y descripción
    list_filter = ('fecha_hora', 'organizador')  # Filtrar por fecha y organizador

admin.site.register(Evento, EventoAdmin)

# Personalización del administrador para el modelo Reserva
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('pk','usuario', 'evento', 'entradas', 'estado')  # Mostrar estas columnas en la lista
    search_fields = ('usuario__username', 'evento__titulo')  # Buscar por nombre de usuario y título del evento
    list_filter = ('estado',)  # Filtrar por estado de la reserva

admin.site.register(Reserva, ReservaAdmin)

# Personalización del administrador para el modelo Comentario
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_creacion', 'texto')  # Mostrar estas columnas en la lista
    search_fields = ('usuario__username', 'evento__titulo', 'texto')  # Buscar por usuario, evento o texto
    list_filter = ('fecha_creacion',)  # Filtrar por fecha de creación

admin.site.register(Comentario, ComentarioAdmin)






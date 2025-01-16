from django.contrib import admin
from .models import UsuarioPersonalizado, Libro, Comentario, Reserva

# Personalización del modelo UsuarioPersonalizado en el admin
@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

# Personalización del modelo Libro en el admin
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion', 'categoria', 'cantidad_disponible')
    list_filter = ('categoria', 'fecha_publicacion')
    search_fields = ('titulo', 'autor', 'categoria')

# Personalización del modelo Comentario en el admin
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'libro', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('usuario__username', 'libro__titulo', 'texto')

# Personalización del modelo Reserva en el admin
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'libro', 'estado', 'fecha_reserva')
    list_filter = ('estado', 'fecha_reserva')
    search_fields = ('usuario__username', 'libro__titulo')

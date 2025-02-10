"""
URL configuration for RestAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eventoapp import views

urlpatterns = [
    path('listar_eventos/', views.listar_eventos, name='listar_eventos'),
    path('crear_evento/', views.crear_evento, name='crear_evento'),  # Nueva ruta para crear eventos,
    path('actualizar_evento/<int:evento_id>/', views.actualizar_evento, name='actualizar_evento'),
    path('eliminar_evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('listar_reservas/', views.listar_reservas, name='listar_reservas'),
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('actualizar_estado_reserva/<int:reserva_id>/<int:usuario_id>/', views.actualizar_estado_reserva, name='actualizar_estado_reserva'),
    path('cancelar_reserva/<int:reserva_id>/<int:usuario_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('listar_comentarios/<int:evento_id>/', views.listar_comentarios, name='listar_comentarios'),
    path('crear_comentario/', views.crear_comentario, name='crear_comentario'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('admin/', admin.site.urls),
]

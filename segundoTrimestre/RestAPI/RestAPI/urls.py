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


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
   openapi.Info(
       title="API Documentación",
       default_version="v1",
       description="Documentación de la API",
   ),
   public=True,
   permission_classes=[AllowAny],
)


from rest_framework.authtoken.views import ObtainAuthToken
from eventoapp.views import (ListarEventosAPIView, ListarReservasAPIView, \
   ListarComentariosAPIView, RegistrarUsuarioAPIView, LoginUsuarioAPIView, CrearComentarioAPIView, CrearReservaAPIView, \
   CrearEventoAPIView, EliminarEventoAPIView, CancelarReservaAPIView, ActualizarEventoAPIView, \
   ActualizarEstadoReservaAPIView)


urlpatterns = [
   path('eventos/', ListarEventosAPIView.as_view(), name='listar_eventos'),
   path('eventos/crear/', CrearEventoAPIView.as_view(), name='crear_evento'),
   path('eventos/<int:evento_id>/', ActualizarEventoAPIView.as_view(), name='actualizar_evento'),
   path('eventos/<int:evento_id>/eliminar/', EliminarEventoAPIView.as_view(), name='eliminar_evento'),
   path('reservas/', ListarReservasAPIView.as_view(), name='listar_reservas'),
   path('reservas/crear/', CrearReservaAPIView.as_view(), name='crear_reserva'),
   path('reservas/<int:reserva_id>/actualizar_estado/',  ActualizarEstadoReservaAPIView.as_view(), name='actualizar_estado_reserva'),
   path('reservas/<int:reserva_id>/eliminar/', CancelarReservaAPIView.as_view(), name='cancelar_reserva'),
   path('comentarios/<int:evento_id>/', ListarComentariosAPIView.as_view(), name='listar_comentarios'),
   path('comentarios/crear/', CrearComentarioAPIView.as_view(), name='crear_comentario'),
   path('login/', ObtainAuthToken.as_view(), name='login_usuario'),
   path('registrar/', RegistrarUsuarioAPIView.as_view(), name='registrar_usuario'),
   path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
]

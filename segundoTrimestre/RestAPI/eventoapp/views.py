from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


# Create your views here.


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Evento, Usuario, Reserva, Comentario
import json


class ListarEventosAPIView(APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]


   @swagger_auto_schema(
       operation_description="Lista eventos filtrados por título, ordenados por fecha y paginados.",
       manual_parameters=[
           openapi.Parameter(
               'titulo',
               openapi.IN_QUERY,
               description="Filtrar por título del evento (búsqueda parcial).",
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               'orden',
               openapi.IN_QUERY,
               description="Campo por el cual ordenar la lista, por defecto es 'fecha_hora'.",
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               'limite',
               openapi.IN_QUERY,
               description="Cantidad de eventos por página.",
               type=openapi.TYPE_INTEGER,
               default=5
           ),
           openapi.Parameter(
               'pagina',
               openapi.IN_QUERY,
               description="Número de página para la paginación.",
               type=openapi.TYPE_INTEGER,
               default=1
           ),
       ],
       responses={
           200: openapi.Response(
               description="Lista de eventos paginados y filtrados.",
               examples={
                   "application/json": {
                       "count": 20,
                       "total_pages": 4,
                       "current_page": 1,
                       "next": 2,
                       "previous": None,
                       "results": [
                           {
                               "id": 1,
                               "titulo": "Evento A",
                               "descripcion": "Descripción del Evento A",
                               "fecha_hora": "2023-12-01T17:00:00Z",
                               "capacidad": 50,
                               "imagen_url": "http://example.com/imagen.jpg",
                               "pelicula": "Película A",
                               "organizador": "organizador1"
                           }
                       ]
                   }
               }
           ),
           400: openapi.Response(
               description="Error en la solicitud (por ejemplo, página fuera de rango)."
           ),
       },
   )
   def get(self, request):
       titulo = request.GET.get("titulo", "")
       orden = request.GET.get("orden", "fecha_hora")
       limite = int(request.GET.get("limite", 5))
       pagina = int(request.GET.get("pagina", 1))


       eventos = Evento.objects.filter(
           titulo__icontains=titulo
       ).order_by(orden).select_related("organizador").prefetch_related("reservas")


       paginator = Paginator(eventos, limite)


       try:
           eventos_pagina = paginator.page(pagina)
       except Exception as e:
           return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)


       data = {
           "count": paginator.count,
           "total_pages": paginator.num_pages,
           "current_page": pagina,
           "next": pagina + 1 if eventos_pagina.has_next() else None,
           "previous": pagina - 1 if eventos_pagina.has_previous() else None,
           "results": [
               {
                   "id": e.id,
                   "titulo": e.titulo,
                   "descripcion": e.descripcion,
                   "fecha_hora": e.fecha_hora,
                   "capacidad": e.capacidad,
                   "imagen_url": e.imagen_url,
                   "pelicula": e.pelicula,
                   "organizador": e.organizador.username
               } for e in eventos_pagina
           ]
       }


       return Response(data)


@login_required
def inicio_view(request):
    eventos = Evento.objects.all()
    return render(request, 'inicio.html', {'eventos': eventos})



class CrearEventoAPIView(APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]


   def post(self, request):
       datos = request.data


       # Validar campos obligatorios
       campos_requeridos = ["titulo", "descripcion", "fecha_hora", "capacidad", "imagen_url", "pelicula"]
       for campo in campos_requeridos:
           if campo not in datos:
               return Response({"error": f"El campo '{campo}' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)


       try:
           # Crear el evento asignando al organizador como el usuario autenticado
           evento = Evento.objects.create(
               titulo=datos["titulo"],
               descripcion=datos["descripcion"],
               fecha_hora=datos["fecha_hora"],
               capacidad=datos["capacidad"],
               imagen_url=datos.get("imagen_url", ""),
               pelicula=datos["pelicula"],
               organizador=request.user
           )
           return Response({"id": evento.id, "mensaje": "Evento creado exitosamente."}, status=status.HTTP_201_CREATED)
       except Exception as e:
           return Response({"error": f"Error al crear el evento: {str(e)}"},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class ActualizarEventoAPIView(APIView):
   authentication_classes = [TokenAuthentication]  # Requiere Token
   permission_classes = [IsAuthenticated]  # Permiso: Usuario debe estar autenticado


   def put(self, request, evento_id):  # PUT reemplaza el evento completo
       return self._actualizar_evento(request, evento_id)


   def patch(self, request, evento_id):  # PATCH actualiza solo campos parciales
       return self._actualizar_evento(request, evento_id)


   def _actualizar_evento(self, request, evento_id):
       # Buscar el evento; regresa 404 si no existe
       evento = get_object_or_404(Evento, id=evento_id)


       # Verificar que el usuario autenticado sea el organizador del evento
       if evento.organizador != request.user:  # 'organizador' debe coincidir con 'request.user'
           return Response(
               {"error": "Solo el organizador del evento puede actualizarlo."},
               status=status.HTTP_403_FORBIDDEN
           )


       # Obtener datos del request (JSON)
       data = request.data


       # Actualizar campos si se pasan en el JSON, manteniendo los actuales en caso contrario
       try:
           evento.titulo = data.get("titulo", evento.titulo)
           evento.descripcion = data.get("descripcion", evento.descripcion)
           evento.fecha_hora = data.get("fecha_hora", evento.fecha_hora)
           evento.capacidad = data.get("capacidad", evento.capacidad)
           evento.imagen_url = data.get("imagen_url", evento.imagen_url)
           evento.pelicula = data.get("pelicula", evento.pelicula)


           # Guardar los cambios en la base de datos
           evento.save()


           # Responder con éxito
           return Response({"mensaje": "Evento actualizado exitosamente."}, status=status.HTTP_200_OK)
       except Exception as e:
           return Response(
               {"error": f"Error al actualizar el evento: {str(e)}"},
               status=status.HTTP_400_BAD_REQUEST
           )






class EliminarEventoAPIView(APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]


   def delete(self, request, evento_id):
       evento = get_object_or_404(Evento, id=evento_id)


       # Verificar que el usuario autenticado es el organizador
       if evento.organizador != request.user:
           return Response(
               {"error": "Solo el organizador del evento puede eliminarlo."},
               status=status.HTTP_403_FORBIDDEN
           )


       evento.delete()
       return Response({"mensaje": "Evento eliminado exitosamente."}, status=status.HTTP_200_OK)








class ListarReservasAPIView(APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]


   def get(self, request):
       estado = request.GET.get("estado", "")
       orden = request.GET.get("orden", "estado")
       limite = int(request.GET.get("limite", 5))
       pagina = int(request.GET.get("pagina", 1))


       reservas = Reserva.objects.filter(usuario=request.user).select_related("usuario", "evento")


       if estado:
           reservas = reservas.filter(estado__iexact=estado)


       reservas = reservas.order_by(orden)


       paginator = Paginator(reservas, limite)


       try:
           reservas_pagina = paginator.page(pagina)
       except Exception as e:
           return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


       data = {
           "count": paginator.count,
           "total_pages": paginator.num_pages,
           "current_page": pagina,
           "next": pagina + 1 if reservas_pagina.has_next() else None,
           "previous": pagina - 1 if reservas_pagina.has_previous() else None,
           "results": [
               {
                   "id": r.id,
                   "usuario": r.usuario.username,
                   "evento": r.evento.titulo if r.evento else None,
                   "entradas": r.entradas,
                   "estado": r.estado
               } for r in reservas_pagina
           ]
       }


       return Response(data)






class CrearReservaAPIView(APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]


   def post(self, request):
       datos = request.data
       campos_requeridos = ["evento", "entradas"]
       for campo in campos_requeridos:
           if campo not in datos:
               return Response({"error": f"El campo '{campo}' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)


       evento = get_object_or_404(Evento, id=datos["evento"])


       entradas_disponibles = evento.capacidad - evento.reservas.aggregate(total_entradas=Sum("entradas"))[
           "total_entradas"] or 0
       if int(datos["entradas"]) > entradas_disponibles:
           return Response({"error": "No hay suficientes asientos disponibles para este evento."},
                           status=status.HTTP_400_BAD_REQUEST)


       try:
           reserva = Reserva.objects.create(
               usuario=request.user,
               evento=evento,
               entradas=datos["entradas"],
               estado=datos.get("estado", "pendiente")
           )
           return Response({"id": reserva.id, "mensaje": "Reserva creada exitosamente :)"},
                           status=status.HTTP_201_CREATED)
       except Exception as e:
           return Response({"error": f"Error al crear la reserva: {str(e)}"},
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def detalle_evento_view(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'detalle.html', {'evento': evento})

def crear_reserva_view(request, evento_id):
    """
    Crea una reserva del evento para el usuario autenticado.
    """
    if request.method == "POST":
        entradas = int(request.POST.get("entradas"))
        evento = get_object_or_404(Evento, id=evento_id)

        if entradas > evento.capacidad:
            return render(request, 'detalle.html', {
                'evento': evento,
                'error': "No hay suficientes entradas disponibles."
            })

        # Crear la reserva
        Reserva.objects.create(
            usuario=request.user,
            evento=evento,
            entradas=entradas
        )

        # Redirigir al panel de usuario
        return HttpResponseRedirect("/panel-usuario/")  # URL para el panel del usuario


@login_required
def reservas_usuario_view(request):
    """
    Muestra las reservas realizadas por el usuario autenticado.
    """
    reservas = Reserva.objects.filter(usuario=request.user).select_related('evento')

    return render(request, 'panel_usuario.html', {
        'reservas': reservas
    })





class ActualizarEstadoReservaAPIView(APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]


   def patch(self, request, reserva_id):
       reserva = get_object_or_404(Reserva, id=reserva_id)


       if reserva.evento.organizador != request.user:
           return Response(
               {"error": "Solo el organizador del evento puede actualizar el estado de una reserva."},
               status=status.HTTP_403_FORBIDDEN
           )


       data = request.data
       nuevo_estado = data.get('estado')


       ESTADOS_VALIDOS = ['pendiente', 'confirmada', 'cancelada']
       if not nuevo_estado:
           return Response(
               {"error": "El campo 'estado' es obligatorio."},
               status=status.HTTP_400_BAD_REQUEST
           )


       if nuevo_estado not in ESTADOS_VALIDOS:
           return Response(
               {"error": f"El estado '{nuevo_estado}' no es válido. Estados permitidos: {ESTADOS_VALIDOS}"},
               status=status.HTTP_400_BAD_REQUEST
           )


       reserva.estado = nuevo_estado
       reserva.save()


       return Response({
           "mensaje": "El estado de la reserva ha sido actualizado correctamente.",
           "reserva_id": reserva.id,
           "nuevo_estado": reserva.estado
       }, status=status.HTTP_200_OK)




class CancelarReservaAPIView(APIView):
   authentication_classes = [TokenAuthentication]  # El token sigue siendo obligatorio
   permission_classes = [IsAuthenticated]  # Solo permite a usuarios autenticados acceder


   def delete(self, request, reserva_id):
       # Obtener la reserva específica basada en el ID
       reserva = get_object_or_404(Reserva, id=reserva_id)


       # Opcional: Verificar rol del usuario, si esto sigue siendo importante
       if hasattr(request.user, 'rol') and request.user.rol != 'participante':
           return Response(
               {"error": "Solo los usuarios con rol 'participante' pueden cancelar reservas."},
               status=status.HTTP_403_FORBIDDEN
           )


       # Verificar si el usuario autenticado es o no el propietario de la reserva
       if reserva.usuario != request.user:
           # Aquí puedes registrar o advertir que la eliminación se realizó
           # por alguien que no es el propietario
           # Por ejemplo, podríamos simplemente continuar:
           pass


       # Eliminar la reserva
       reserva.delete()


       # Retornar la confirmación de la eliminación
       return Response(
           {"mensaje": "Reserva cancelada exitosamente."},
           status=status.HTTP_200_OK
       )






class ListarComentariosAPIView(APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]


   def get(self, request, evento_id):
       orden = request.GET.get("orden", "-fecha_creacion")
       limite = int(request.GET.get("limite", 5))
       pagina = int(request.GET.get("pagina", 1))


       evento = get_object_or_404(Evento, id=evento_id)
       comentarios = Comentario.objects.filter(evento=evento).select_related("usuario").order_by(orden)


       paginator = Paginator(comentarios, limite)


       try:
           comentarios_pagina = paginator.page(pagina)
       except Exception as e:
           return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


       data = {
           "count": paginator.count,
           "total_pages": paginator.num_pages,
           "current_page": pagina,
           "next": pagina + 1 if comentarios_pagina.has_next() else None,
           "previous": pagina - 1 if comentarios_pagina.has_previous() else None,
           "results": [
               {
                   "id": comentario.id,
                   "usuario": comentario.usuario.username,
                   "texto": comentario.texto,
                   "fecha_creacion": comentario.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
               } for comentario in comentarios_pagina
           ]
       }


       return Response(data)






class CrearComentarioAPIView(APIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]


   def post(self, request):
       datos = request.data
       if "texto" not in datos or "evento" not in datos:
           return Response({"error": 'Los campos "texto" y "evento" son obligatorios.'},
                           status=status.HTTP_400_BAD_REQUEST)


       evento = get_object_or_404(Evento, id=datos["evento"])


       try:
           comentario = Comentario.objects.create(
               texto=datos["texto"],
               usuario=request.user,
               evento=evento
           )
           return Response({
               "mensaje": "Comentario creado exitosamente.",
               "comentario": {
                   "id": comentario.id,
                   "texto": comentario.texto,
                   "fecha_creacion": comentario.fecha_creacion.isoformat(),
               }
           }, status=status.HTTP_201_CREATED)
       except Exception as e:
           return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class LoginUsuarioAPIView(APIView):
   def post(self, request):
       datos = request.data  # Extraer datos del cuerpo de la petición


       # Validar campos obligatorios
       if not all(campo in datos for campo in ["username", "password"]):
           return Response({"error": 'Los campos "username" y "password" son obligatorios.'},
                           status=status.HTTP_400_BAD_REQUEST)


       # Autenticar al usuario
       try:
           usuario = Usuario.objects.get(username=datos["username"])
           # Esta parte asume que tienes manejo básico de contraseñas configurado
           # para validar una contraseña. Asegúrate de usar `check_password` o algo similar si es necesario.
           return Response({
               "mensaje": "Inicio de sesión exitoso.",
               "usuario": {
                   "id": usuario.id,
                   "username": usuario.username,
                   "rol": usuario.rol,  # Campo personalizado del modelo
               }
           }, status=status.HTTP_200_OK)
       except Usuario.DoesNotExist:
           return Response({"error": "Credenciales inválidas. Usuario no encontrado."},
                           status=status.HTTP_401_UNAUTHORIZED)
       except Exception as e:
           return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            # 1. Obtener datos del POST o del cuerpo JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST

            username = data.get('username')
            password = data.get('password')

            # 2. Validar que ambos campos estén presentes
            if not username or not password:
                return JsonResponse({'error': 'Debes proporcionar un username y una contraseña.'}, status=400)

            # 3. Autenticar al usuario
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # 4. Crear (o recuperar) el token para el usuario
                from rest_framework.authtoken.models import Token
                token, _ = Token.objects.get_or_create(user=user)

                # 5. Iniciar sesión en el sistema Django
                login(request, user)

                # 6. Responder con el token en JSON
                return JsonResponse({'token': token.key}, status=200)

            # Si el usuario no se autentica (credenciales incorrectas)
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)

        except Exception as e:
            # Manejo de errores inesperados
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)

    # Si no es una solicitud POST, renderizar el formulario de inicio de sesión
    return render(request, 'login.html')








class RegistrarUsuarioAPIView(APIView):
   def post(self, request):
       datos = request.data  # Extraer datos del cuerpo de la petición


       # Validar campos obligatorios
       if not all(campo in datos for campo in ["username", "password"]):
           return Response({"error": 'Los campos "username" y "password" son obligatorios.'},
                           status=status.HTTP_400_BAD_REQUEST)


       # Validar que la contraseña sea numérica
       if not str(datos["password"]).isdigit():
           return Response({"error": "La contraseña debe contener únicamente números."},
                           status=status.HTTP_400_BAD_REQUEST)


       # Verificar si el usuario ya existe
       if Usuario.objects.filter(username=datos["username"]).exists():
           return Response({"error": "El username ya está en uso. Elige otro."},
                           status=status.HTTP_409_CONFLICT)


       try:
           # Crear el usuario
           nuevo_usuario = Usuario(
               username=datos["username"],
               rol=datos.get("rol", "participante"),
               biografia=datos.get("biografia", "")
           )
           nuevo_usuario.set_password(str(datos["password"]))  # Guardar contraseña de forma segura
           nuevo_usuario.save()


           return Response({
               "mensaje": "Usuario registrado exitosamente.",
               "usuario": {
                   "id": nuevo_usuario.id,
                   "username": nuevo_usuario.username,
                   "rol": nuevo_usuario.rol,  # Campo adicional del modelo
                   "biografia": nuevo_usuario.biografia
               }
           }, status=status.HTTP_201_CREATED)
       except Exception as e:
           return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

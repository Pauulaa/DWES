# TokenAuthentication permite autenticar las solicitudes utilizando un token (por ejemplo, un JWT)
from rest_framework.authentication import TokenAuthentication  

# IsAuthenticated es una clase de permiso que asegura que solo los usuarios autenticados puedan acceder a las vistas
from rest_framework.permissions import IsAuthenticated  

# Response es utilizado para devolver respuestas HTTP personalizadas en formato JSON en tus vistas
from rest_framework.response import Response  

# APIView es una clase base para crear vistas que usen la arquitectura de Django REST Framework
from rest_framework.views import APIView  

# Importación de constantes de estado HTTP para manejar los errores de forma más clara
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND  

# Paginator es utilizado para dividir listas de objetos en páginas
from django.core.paginator import Paginator  

# Sum es una función para calcular la suma de valores, por ejemplo, para contar las reservas de un evento
from django.db.models import Sum  

# get_object_or_404 es una utilidad que busca un objeto, y si no lo encuentra, devuelve un error 404 automáticamente
from django.shortcuts import get_object_or_404  

# render se utiliza para renderizar plantillas HTML en las vistas de Django
from django.shortcuts import render  

# Utilidades para generar documentación Swagger de tu API
from drf_yasg.utils import swagger_auto_schema  

# openapi es usado para definir detalles adicionales sobre los parámetros y respuestas de las vistas para la documentación Swagger
from drf_yasg import openapi  

# status es un módulo que contiene constantes relacionadas con los códigos de estado HTTP
from rest_framework import status  

# HttpResponseRedirect permite redirigir al usuario a otra URL
from django.http import HttpResponseRedirect  

# authenticate y login son funciones de Django que permiten autenticar un usuario y crear una sesión para él
from django.contrib.auth import authenticate, login  

# Decoradores de Django para habilitar la CSRF o exigir que un usuario esté autenticado para acceder a la vista
from django.views.decorators.csrf import csrf_exempt  # Usado para permitir solicitudes sin protección CSRF (generalmente no recomendado para producción)
from django.contrib.auth.decorators import login_required  # Usado para requerir que un usuario esté autenticado antes de ejecutar la vista

# Importación de los modelos de la aplicación, como Evento, Usuario, Reserva y Comentario
from .models import Evento, Usuario, Reserva, Comentario  

# json es una librería estándar de Python para trabajar con datos en formato JSON (por ejemplo, convertir entre diccionarios y JSON)
import json 

class ListarEventosAPIView(APIView):  # Vista para listar eventos
    authentication_classes = [TokenAuthentication]  # Requiere autenticación con token
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

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
                        "count": 20,  # Total de eventos
                        "total_pages": 4,  # Total de páginas
                        "current_page": 1,  # Página actual
                        "next": 2,  # Página siguiente
                        "previous": None,  # Página anterior
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
    def get(self, request):  # Método GET para obtener la lista de eventos
        # Obtener los parámetros de la solicitud
        titulo = request.GET.get("titulo", "")  # Filtrar por título (búsqueda parcial)
        orden = request.GET.get("orden", "fecha_hora")  # Ordenar por fecha de evento por defecto
        limite = int(request.GET.get("limite", 5))  # Número de eventos por página (por defecto 5)
        pagina = int(request.GET.get("pagina", 1))  # Número de página para la paginación (por defecto 1)

        # Filtrar eventos por título y ordenar por el campo proporcionado
        eventos = Evento.objects.filter(
            titulo__icontains=titulo  # Filtrar eventos cuyo título contenga la palabra clave
        ).order_by(orden).select_related("organizador").prefetch_related("reservas")

        # Paginación: dividir los eventos en páginas según el límite
        paginator = Paginator(eventos, limite)

        try:
            # Obtener la página solicitada
            eventos_pagina = paginator.page(pagina)
        except Exception as e:
            # Si hay un error en la paginación, devolver un error 400
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Crear la respuesta con los eventos paginados
        data = {
            "count": paginator.count,  # Total de eventos encontrados
            "total_pages": paginator.num_pages,  # Total de páginas
            "current_page": pagina,  # Página actual
            "next": pagina + 1 if eventos_pagina.has_next() else None,  # Página siguiente
            "previous": pagina - 1 if eventos_pagina.has_previous() else None,  # Página anterior
            "results": [
                {
                    "id": e.id,
                    "titulo": e.titulo,  # Título del evento
                    "descripcion": e.descripcion,  # Descripción del evento
                    "fecha_hora": e.fecha_hora,  # Fecha y hora del evento
                    "capacidad": e.capacidad,  # Capacidad del evento
                    "imagen_url": e.imagen_url,  # URL de la imagen del evento
                    "pelicula": e.pelicula,  # Película asociada (si aplica)
                    "organizador": e.organizador.username  # Nombre de usuario del organizador
                } for e in eventos_pagina  # Para cada evento en la página actual
            ]
        }

        # Responder con los datos de los eventos paginados
        return Response(data)


def inicio_view(request):  # Vista para renderizar la página de inicio
    eventos = Evento.objects.all()  # Obtener todos los eventos
    return render(request, 'inicio.html', {'eventos': eventos})  # Renderizar la plantilla con los eventos


class CrearEventoAPIView(APIView):  # Vista para crear un nuevo evento
    authentication_classes = [TokenAuthentication]  # Requiere autenticación con token
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def post(self, request):  # Método POST para crear un evento
        datos = request.data  # Obtener los datos del cuerpo de la solicitud

        # Validar que los campos obligatorios estén presentes
        campos_requeridos = ["titulo", "descripcion", "fecha_hora", "capacidad", "imagen_url", "pelicula"]
        for campo in campos_requeridos:
            if campo not in datos:
                # Si falta algún campo obligatorio, devolver un error 400
                return Response({"error": f"El campo '{campo}' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crear el nuevo evento asignando al organizador como el usuario autenticado
            evento = Evento.objects.create(
                titulo=datos["titulo"],
                descripcion=datos["descripcion"],
                fecha_hora=datos["fecha_hora"],
                capacidad=datos["capacidad"],
                imagen_url=datos.get("imagen_url", ""),
                pelicula=datos["pelicula"],
                organizador=request.user  # El organizador es el usuario autenticado
            )
            # Responder con el ID del evento y un mensaje de éxito
            return Response({"id": evento.id, "mensaje": "Evento creado exitosamente."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Si ocurre algún error al crear el evento, devolver un error 500
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






class EliminarEventoAPIView(APIView):  # Vista para eliminar eventos
    authentication_classes = [TokenAuthentication]  # Requiere autenticación con token
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def delete(self, request, evento_id):  # Método DELETE para eliminar un evento
        # Obtener el evento o devolver un error 404 si no existe
        evento = get_object_or_404(Evento, id=evento_id)

        # Verificar si el usuario autenticado es el organizador del evento
        if evento.organizador != request.user:
            return Response(
                {"error": "Solo el organizador del evento puede eliminarlo."},
                status=status.HTTP_403_FORBIDDEN  # Código 403: Prohibido
            )

        # Eliminar el evento de la base de datos
        evento.delete()

        # Responder con un mensaje de éxito
        return Response({"mensaje": "Evento eliminado exitosamente."}, status=status.HTTP_200_OK)  # Código 200: Éxito



class ListarReservasAPIView(APIView):  # Vista para listar las reservas del usuario
    authentication_classes = [TokenAuthentication]  # Requiere autenticación con token
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request):  # Método GET para listar las reservas
        # Obtener parámetros opcionales de la solicitud
        estado = request.GET.get("estado", "")  # Filtro por estado de la reserva (opcional)
        orden = request.GET.get("orden", "estado")  # Filtro por orden (por defecto por estado)
        limite = int(request.GET.get("limite", 5))  # Número de resultados por página (por defecto 5)
        pagina = int(request.GET.get("pagina", 1))  # Número de página (por defecto 1)

        # Filtrar reservas del usuario autenticado
        reservas = Reserva.objects.filter(usuario=request.user).select_related("usuario", "evento")

        # Si se proporciona un estado, filtrar las reservas por ese estado
        if estado:
            reservas = reservas.filter(estado__iexact=estado)

        # Ordenar las reservas según el campo especificado
        reservas = reservas.order_by(orden)

        # Paginación: dividir las reservas en páginas según el límite
        paginator = Paginator(reservas, limite)

        try:
            # Obtener la página de reservas correspondiente
            reservas_pagina = paginator.page(pagina)
        except Exception as e:
            # Si hay un error en la paginación, devolver un error 400
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Crear la estructura de datos para la respuesta
        data = {
            "count": paginator.count,  # Total de reservas
            "total_pages": paginator.num_pages,  # Total de páginas
            "current_page": pagina,  # Página actual
            "next": pagina + 1 if reservas_pagina.has_next() else None,  # Página siguiente (si existe)
            "previous": pagina - 1 if reservas_pagina.has_previous() else None,  # Página anterior (si existe)
            "results": [
                {
                    "id": r.id,
                    "usuario": r.usuario.username,  # Nombre de usuario que hizo la reserva
                    "evento": r.evento.titulo if r.evento else None,  # Título del evento
                    "entradas": r.entradas,  # Número de entradas reservadas
                    "estado": r.estado  # Estado de la reserva
                } for r in reservas_pagina  # Para cada reserva en la página actual
            ]
        }

        # Devolver la respuesta con la lista paginada de reservas
        return Response(data)






class CrearReservaAPIView(APIView):  # Vista para crear reservas
    authentication_classes = [TokenAuthentication]  # Requiere autenticación con token
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def post(self, request):  # Método POST para crear una reserva
        datos = request.data  # Obtener datos enviados en la solicitud

        # Lista de campos obligatorios
        campos_requeridos = ["evento", "entradas"]
        for campo in campos_requeridos:
            if campo not in datos:
                return Response(
                    {"error": f"El campo '{campo}' es obligatorio."},
                    status=status.HTTP_400_BAD_REQUEST  # Código 400: Solicitud incorrecta
                )

        # Obtener el evento o devolver un error 404 si no existe
        evento = get_object_or_404(Evento, id=datos["evento"])

        # Calcular el número de entradas disponibles
        entradas_reservadas = evento.reservas.aggregate(total_entradas=Sum("entradas"))["total_entradas"] or 0
        entradas_disponibles = evento.capacidad - entradas_reservadas  # Restar las reservadas a la capacidad total

        # Validar si hay suficientes asientos disponibles
        if int(datos["entradas"]) > entradas_disponibles:
            return Response(
                {"error": "No hay suficientes asientos disponibles para este evento."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Crear la reserva
            reserva = Reserva.objects.create(
                usuario=request.user,  # Asignar el usuario autenticado
                evento=evento,  # Asignar el evento
                entradas=datos["entradas"],  # Cantidad de entradas solicitadas
                estado=datos.get("estado", "pendiente")  # Estado por defecto: "pendiente"
            )

            # Responder con éxito y devolver el ID de la reserva creada
            return Response(
                {"id": reserva.id, "mensaje": "Reserva creada exitosamente :)"},
                status=status.HTTP_201_CREATED  # Código 201: Creado exitosamente
            )
        except Exception as e:
            # Manejar cualquier error inesperado
            return Response(
                {"error": f"Error al crear la reserva: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR  # Código 500: Error del servidor
            )


def detalle_evento_view(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'detalle.html', {'evento': evento})

def crear_reserva_view(request):
    """
    Crea una reserva para el evento que está siendo visualizado.
    """
    if request.method == "POST":
        # Obtener el contexto del evento actual desde la URL o sesión
        evento_id = request.session.get('evento_id')  # Supongamos que lo guardas en la sesión
        evento = get_object_or_404(Evento, id=evento_id)

        # Leer la cantidad en el cuerpo de la solicitud (es JSON en el frontend)
        body = json.loads(request.body)
        entradas = int(body.get("cantidad"))

        # Validar si hay suficientes entradas disponibles
        if entradas > evento.capacidad:
            return render(request, 'detalle.html', {
                'evento': evento,
                'error': "No hay suficientes entradas disponibles."
            })

        # Crear la reserva
        Reserva.objects.create(
            usuario=request.user,  # Usuario autenticado
            evento=evento,
            entradas=entradas
        )

        # Redirigir al panel del usuario
        return HttpResponseRedirect("/panel_usuario/")  # Cambia esto si tu panel tiene otra ruta

    return render(request, 'detalle.html', {
        'error': "Método no permitido.",
    })


def detalle_evento_view(request, evento_id):
    """
    Renderiza los detalles de un evento.
    """
    evento = get_object_or_404(Evento, id=evento_id)

    # Guarda el ID del evento en la sesión
    request.session['evento_id'] = evento.id

    # Renderiza la página de detalles
    return render(request, 'detalle.html', {'evento': evento})




@login_required
def reservas_usuario_view(request):
    """
    Muestra las reservas realizadas por el usuario autenticado.
    """
    reservas = Reserva.objects.filter(usuario=request.user).select_related('evento')

    return render(request, 'panel_usuario.html', {
        'reservas': reservas
    })





class ActualizarEstadoReservaAPIView(APIView):  # Vista basada en clases para actualizar reservas
    authentication_classes = [TokenAuthentication]  # Requiere autenticación con token
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def patch(self, request, reserva_id):  # Método PATCH para actualizar parcialmente una reserva
        # Obtener la reserva o devolver un error 404 si no existe
        reserva = get_object_or_404(Reserva, id=reserva_id)

        # Verificar si el usuario autenticado es el organizador del evento de la reserva
        if reserva.evento.organizador != request.user:
            return Response(
                {"error": "Solo el organizador del evento puede actualizar el estado de una reserva."},
                status=status.HTTP_403_FORBIDDEN  # Código 403: Prohibido
            )

        data = request.data  # Extraer los datos enviados en la solicitud
        nuevo_estado = data.get('estado')  # Obtener el nuevo estado de la reserva

        # Lista de estados válidos
        ESTADOS_VALIDOS = ['pendiente', 'confirmada', 'cancelada']

        # Validar que el campo "estado" no esté vacío
        if not nuevo_estado:
            return Response(
                {"error": "El campo 'estado' es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST  # Código 400: Solicitud incorrecta
            )

        # Validar que el estado proporcionado sea uno de los permitidos
        if nuevo_estado not in ESTADOS_VALIDOS:
            return Response(
                {"error": f"El estado '{nuevo_estado}' no es válido. Estados permitidos: {ESTADOS_VALIDOS}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Actualizar el estado de la reserva
        reserva.estado = nuevo_estado
        reserva.save()  # Guardar los cambios en la base de datos

        # Responder con un mensaje de éxito y los datos actualizados
        return Response({
            "mensaje": "El estado de la reserva ha sido actualizado correctamente.",
            "reserva_id": reserva.id,
            "nuevo_estado": reserva.estado
        }, status=status.HTTP_200_OK)  # Código 200: Éxito




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






class ListarComentariosAPIView(APIView):  # Vista basada en clases para listar comentarios
    authentication_classes = [TokenAuthentication]  # Requiere autenticación por token
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request, evento_id):  # Método para manejar solicitudes GET
        # Obtener parámetros opcionales de la URL con valores predeterminados
        orden = request.GET.get("orden", "-fecha_creacion")  # Ordenamiento (por defecto, descendente por fecha)
        limite = int(request.GET.get("limite", 5))  # Límite de comentarios por página (por defecto, 5)
        pagina = int(request.GET.get("pagina", 1))  # Número de página (por defecto, 1)

        # Buscar el evento en la base de datos, o devolver un error 404 si no existe
        evento = get_object_or_404(Evento, id=evento_id)

        # Filtrar comentarios asociados al evento, incluyendo datos del usuario relacionado
        comentarios = Comentario.objects.filter(evento=evento).select_related("usuario").order_by(orden)

        # Aplicar paginación a los comentarios
        paginator = Paginator(comentarios, limite)

        try:
            comentarios_pagina = paginator.page(pagina)  # Obtener la página solicitada
        except Exception as e:
            # Si la página solicitada no existe, devolver un error 400
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Construir la respuesta con la información de paginación y los comentarios
        data = {
            "count": paginator.count,  # Total de comentarios
            "total_pages": paginator.num_pages,  # Número total de páginas
            "current_page": pagina,  # Página actual
            "next": pagina + 1 if comentarios_pagina.has_next() else None,  # Número de la siguiente página (si existe)
            "previous": pagina - 1 if comentarios_pagina.has_previous() else None,  # Número de la página anterior (si existe)
            "results": [  # Lista de comentarios en la página actual
                {
                    "id": comentario.id,
                    "usuario": comentario.usuario.username,  # Nombre de usuario del autor
                    "texto": comentario.texto,  # Contenido del comentario
                    "fecha_creacion": comentario.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")  # Formato de fecha legible
                } for comentario in comentarios_pagina
            ]
        }

        return Response(data)  # Devolver la respuesta en formato JSON






class CrearComentarioAPIView(APIView):  # Vista basada en clases para crear comentarios
    authentication_classes = [TokenAuthentication]  # Requiere autenticación por token
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden comentar

    def post(self, request):  # Método para manejar solicitudes POST
        datos = request.data  # Extraer los datos enviados en la petición

        # Validar que los campos "texto" y "evento" estén presentes en la solicitud
        if "texto" not in datos or "evento" not in datos:
            return Response(
                {"error": 'Los campos "texto" y "evento" son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar el evento al que se quiere asociar el comentario
        evento = get_object_or_404(Evento, id=datos["evento"])

        try:
            # Crear un nuevo comentario en la base de datos
            comentario = Comentario.objects.create(
                texto=datos["texto"],  # Contenido del comentario
                usuario=request.user,  # Usuario autenticado que hace el comentario
                evento=evento  # Evento asociado al comentario
            )

            # Respuesta exitosa con los detalles del comentario creado
            return Response({
                "mensaje": "Comentario creado exitosamente.",
                "comentario": {
                    "id": comentario.id,
                    "texto": comentario.texto,
                    "fecha_creacion": comentario.fecha_creacion.isoformat(),  # Formato ISO para la fecha
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Capturar cualquier error inesperado y devolver un mensaje de error
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class LoginUsuarioAPIView(APIView):  # Vista basada en clases para manejar el inicio de sesión
    def post(self, request):  # Método para manejar solicitudes POST
        datos = request.data  # Extraer los datos enviados en la petición

        # Validar que los campos "username" y "password" estén presentes en la petición
        if not all(campo in datos for campo in ["username", "password"]):
            return Response(
                {"error": 'Los campos "username" y "password" son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Intentar autenticar al usuario
        try:
            usuario = Usuario.objects.get(username=datos["username"])  # Buscar usuario en la base de datos

            return Response({
                "mensaje": "Inicio de sesión exitoso.",
                "usuario": {
                    "id": usuario.id,
                    "username": usuario.username,
                    "rol": usuario.rol,  # Campo adicional del modelo
                }
            }, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            # Responder con error si el usuario no existe
            return Response(
                {"error": "Credenciales inválidas. Usuario no encontrado."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as e:
            # Capturar cualquier otro error inesperado
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def login_view(request):
    """
    Vista para renderizar la página de inicio de sesión.
    """
    return render(request, 'login.html')  # Renderiza el template HTML de login


class RegistrarUsuarioAPIView(APIView):  # Vista basada en clases para registrar un usuario
    def post(self, request):  # Método para manejar solicitudes POST
        datos = request.data  # Extraer los datos enviados en la petición

        # Validar que los campos "username" y "password" estén presentes en la petición
        if not all(campo in datos for campo in ["username", "password"]):
            return Response(
                {"error": 'Los campos "username" y "password" son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar que la contraseña contenga solo números
        if not str(datos["password"]).isdigit():
            return Response(
                {"error": "La contraseña debe contener únicamente números."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar si el usuario ya existe en la base de datos
        if Usuario.objects.filter(username=datos["username"]).exists():
            return Response(
                {"error": "El username ya está en uso. Elige otro."},
                status=status.HTTP_409_CONFLICT
            )

        try:
            # Crear una nueva instancia del modelo Usuario con los datos proporcionados
            nuevo_usuario = Usuario(
                username=datos["username"],
                rol=datos.get("rol", "participante"),  # Si no se proporciona, asigna "participante" por defecto
                biografia=datos.get("biografia", "")  # Si no se proporciona, asigna una cadena vacía por defecto
            )
            nuevo_usuario.set_password(str(datos["password"]))  # Guardar la contraseña de forma segura (hashing)
            nuevo_usuario.save()  # Guardar el usuario en la base de datos

            # Respuesta exitosa con los datos del nuevo usuario
            return Response({
                "mensaje": "Usuario registrado exitosamente.",
                "usuario": {
                    "id": nuevo_usuario.id,
                    "username": nuevo_usuario.username,
                    "rol": nuevo_usuario.rol,  # Incluir el rol en la respuesta
                    "biografia": nuevo_usuario.biografia  # Incluir la biografía en la respuesta
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Capturar cualquier error inesperado y devolver un mensaje de error
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

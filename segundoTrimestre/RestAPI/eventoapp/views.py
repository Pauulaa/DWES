from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Evento, Usuario, Reserva, Comentario
import json

def listar_eventos(request):
    # Parámetros de filtro y paginación
    titulo = request.GET.get("titulo", "")  # Filtrar por título
    orden = request.GET.get("orden", "fecha_hora")  # Ordenar por el campo especificado
    limite = int(request.GET.get("limite", 5))  # Resultados por página
    pagina = int(request.GET.get("pagina", 1))  # Página actual

    # Filtrar y ordenar eventos
    eventos = Evento.objects.filter(titulo__icontains=titulo).order_by(orden).select_related(
        "organizador").prefetch_related("reservas")
    # Paginación
    paginator = Paginator(eventos, limite)  # Dividir eventos en páginas de tamaño `limite`

    try:
        eventos_pagina = paginator.page(pagina)  # Obtener los eventos de la página actual
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)  # Manejar errores de paginación

    # Crear respuesta con datos paginados
    data = {
        "count": paginator.count,  # Número total de eventos
        "total_pages": paginator.num_pages,  # Número total de páginas
        "current_page": pagina,  # Página actual
        "next": pagina + 1 if eventos_pagina.has_next() else None,  # Página siguiente
        "previous": pagina - 1 if eventos_pagina.has_previous() else None,  # Página anterior
        "results": [
            {"id": e.id, "titulo": e.titulo, "descripcion": e.descripcion, "fecha_hora": e.fecha_hora, "capacidad": e.capacidad, "imagen_url": e.imagen_url, "pelicula": e.pelicula, "organizador": e.organizador.username}
            for e in eventos_pagina
        ]  # Resultados actuales
    }

    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_evento(request):
    if request.method == "POST":
        try:
            # Intentar decodificar el cuerpo de la solicitud como JSON
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Se esperaba un JSON válido"}, status=400)

        # Verificar que todos los campos requeridos estén presentes
        campos_requeridos = ["titulo", "descripcion", "fecha_hora", "capacidad", "imagen_url", "pelicula", "organizador"]
        for campo in campos_requeridos:
            if campo not in data:
                return JsonResponse({"error": f"El campo '{campo}' es obligatorio"}, status=400)

 # Intentar crear el evento
        try:
            # Verificar si el organizador especificado existe
            if not Usuario.objects.filter(username=data['organizador']).exists():
                return JsonResponse({"error": "El organizador especificado no existe"}, status=404)

            # Obtener la instancia del organizador
            organizador = Usuario.objects.get(username=data['organizador'])

            # Crear el evento
            evento = Evento.objects.create(
                titulo=data["titulo"],
                descripcion=data["descripcion"],
                fecha_hora=data["fecha_hora"],
                capacidad=data["capacidad"],
                imagen_url=data.get("imagen_url", ""),  # El campo imagen_url es opcional
                pelicula=data["pelicula"],
                organizador=organizador  # Aquí pasamos la instancia de Usuario
            )

            # Respuesta exitosa
            return JsonResponse({"id": evento.id, "mensaje": "Evento creado exitosamente :)"}, status=201)

        except Exception as e:
            # Error general al crear el evento
            return JsonResponse({"error": f"Error al crear el evento: {str(e)}"}, status=500)

    # Si el método no es POST
    return JsonResponse({"error": "Método no permitido. Use POST"}, status=405)


@csrf_exempt
def actualizar_evento(request, evento_id):
    if request.method in ["PUT", "PATCH"]:
        try:
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist:
            return JsonResponse({"error": "El evento especificado no existe"}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Se esperaba un JSON válido"}, status=400)

        # Verificar que el organizador es el usuario realizando la solicitud
        nuevo_organizador = data.get('organizador')
        if nuevo_organizador and nuevo_organizador != evento.organizador_id:
            return JsonResponse({"error": "Solo el organizador del evento puede actualizarlo"}, status=403)
    try:
        # Actualizar solo los campos proporcionados en la solicitud
        evento.titulo = data.get("titulo", evento.titulo)
        evento.descripcion = data.get("descripcion", evento.descripcion)
        evento.fecha_hora = data.get("fecha_hora", evento.fecha_hora)
        evento.capacidad = data.get("capacidad", evento.capacidad)
        evento.imagen_url = data.get("imagen_url", evento.imagen_url)
        evento.pelicula = data.get("pelicula", evento.pelicula)

        # Guardar los cambios en la base de datos
        evento.save()

        # Respuesta exitosa
        return JsonResponse({"mensaje": "Evento actualizado exitosamente"}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Error al actualizar el evento: {str(e)}"}, status=400)

    # Si el método no es PUT ni PATCH, devolver 405
    return JsonResponse({"error": "Método no permitido. Use PUT o PATCH"}, status=405)


@csrf_exempt
def eliminar_evento(request, evento_id):
    if request.method == "DELETE":
        try:
            # Buscar el evento por su ID
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist:
            return JsonResponse({"error": "El evento especificado no existe"}, status=404)

        try:
            # Cargar el body enviado por el cliente como JSON
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Se esperaba un JSON válido"}, status=400)

        # Verificar que el organizador es el usuario realizando la solicitud
        nuevo_organizador = data.get('organizador')
        if nuevo_organizador and nuevo_organizador != evento.organizador_id:
            return JsonResponse({"error": "Solo el organizador del evento puede eliminarlo"}, status=403)

        # Eliminar el evento una vez validado
        evento.delete()
        return JsonResponse({"mensaje": "Evento eliminado exitosamente"}, status=200)

    # Si el método HTTP no es DELETE
    return JsonResponse({"error": "Método no permitido. Use DELETE para esta acción."}, status=405)


def listar_reservas(request):
    # Parámetros de filtro y paginación
    usuario = request.GET.get("usuario", "")  # Filtrar por usuario (username)
    estado = request.GET.get("estado", "")  # Filtrar por estado
    orden = request.GET.get("orden", "estado")  # Ordenar por el campo especificado
    limite = int(request.GET.get("limite", 5))  # Resultados por página
    pagina = int(request.GET.get("pagina", 1))  # Página actual

    # Filtrar y ordenar reservas
    reservas = Reserva.objects.all().select_related("usuario", "evento")

    if usuario:
        reservas = reservas.filter(usuario__username__icontains=usuario)
    if estado:
        reservas = reservas.filter(estado__iexact=estado)

    reservas = reservas.order_by(orden)

    # Paginación
    paginator = Paginator(reservas, limite)

    try:
        reservas_pagina = paginator.page(pagina)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    # Crear respuesta con datos paginados
    data = {
        "count": paginator.count,  # Número total de reservas
        "total_pages": paginator.num_pages,  # Número total de páginas
        "current_page": pagina,  # Página actual
        "next": pagina + 1 if reservas_pagina.has_next() else None,  # Página siguiente
        "previous": pagina - 1 if reservas_pagina.has_previous() else None,  # Página anterior
        "results": [
            {
                "id": r.id,
                "usuario": r.usuario.username,
                "evento": r.evento.titulo if r.evento else None,
                "entradas": r.entradas,
                "estado": r.estado
            }
            for r in reservas_pagina
        ]
    }

    return JsonResponse(data, safe=False)



@csrf_exempt
def crear_reserva(request):
    if request.method == "POST":
        try:
            # Intentar decodificar el cuerpo de la solicitud como JSON
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Se esperaba un JSON válido"}, status=400)

        # Verificar que todos los campos requeridos estén presentes
        campos_requeridos = ["usuario", "evento", "entradas"]
        for campo in campos_requeridos:
            if campo not in data:
                return JsonResponse({"error": f"El campo '{campo}' es obligatorio"}, status=400)

        # Intentar crear la reserva
        try:
            # Verificar si el usuario especificado existe
            if not Usuario.objects.filter(username=data['usuario']).exists():
                return JsonResponse({"error": "El usuario especificado no existe"}, status=404)

            # Verificar si el evento especificado existe
            if not Evento.objects.filter(id=data['evento']).exists():
                return JsonResponse({"error": "El evento especificado no existe"}, status=404)

            # Obtener instancias del usuario y del evento
            usuario = Usuario.objects.select_related().get(username=data['usuario'])
            evento = Evento.objects.select_related().get(id=data['evento'])

            # Carga las reservas relacionadas al evento
            entradas_disponibles = evento.capacidad - evento.reservas.aggregate(total_entradas=Sum('entradas'))[
                'total_entradas'] or 0
            if int(data["entradas"]) > entradas_disponibles:
                return JsonResponse({"error": "No hay suficientes asientos disponibles para este evento"}, status=400)

            # Crear la reserva
            reserva = Reserva.objects.create(
                usuario=usuario,
                evento=evento,
                entradas=data["entradas"],
                estado=data.get("estado", "pendiente")  # Estado es opcional, por defecto es 'pendiente'
            )

            # Respuesta exitosa
            return JsonResponse({"id": reserva.id, "mensaje": "Reserva creada exitosamente :)"},
                                status=201)

        except Exception as e:
            # Error general al crear la reserva
            return JsonResponse({"error": f"Error al crear la reserva: {str(e)}"}, status=500)

    # Si el método no es POST
    return JsonResponse({"error": "Método no permitido. Use POST"}, status=405)


@csrf_exempt
def actualizar_estado_reserva(request, reserva_id, usuario_id):
    if request.method == 'PATCH':
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Se esperaba un JSON válido"}, status=400)

        nuevo_organizador = data.get('organizador')
        if nuevo_organizador and nuevo_organizador != Reserva.organizador_id:
            return JsonResponse({"error": "Solo el organizador del evento puede actualizarlo"}, status=403)

        nuevo_estado = data['estado']
        ESTADO_VALIDO = ['pendiente', 'confirmada', 'cancelada']
        if nuevo_estado not in ESTADO_VALIDO:
            return JsonResponse(
                {"error": f"El estado '{nuevo_estado}' no es válido. Estados permitidos: {ESTADO_VALIDO}"}, status=400)

        try:
            reserva = Reserva.objects.get(id=reserva_id)
        except Reserva.DoesNotExist:
            return JsonResponse({"error": "La reserva especificada no existe"}, status=404)

        nuevo_estado = data['estado']
        reserva.estado = nuevo_estado
        reserva.save()

        return JsonResponse({
            "mensaje": "El estado de la reserva ha sido actualizado correctamente",
            "reserva_id": reserva.id,
            "nuevo_estado": reserva.estado
        }, status=200)

    return JsonResponse({"error": "Método no permitido. Use PATCH"}, status=405)


@csrf_exempt
def cancelar_reserva(request, reserva_id, usuario_id):
    if request.method == "DELETE":
        try:
            # Buscar la reserva por su ID
            reserva = Reserva.objects.get(id=reserva_id)
        except Reserva.DoesNotExist:
            return JsonResponse({"error": "La reserva especificada no existe"}, status=404)

        #comprobar que el usuario de la reserva es que la está cancelando
        if reserva.usuario.id != usuario_id:
            return JsonResponse({"error": "Solo el usuario que realizó la reserva puede cancelarla"}, status=403)

        # Cancelar o eliminar la reserva (según las reglas de negocio puedes eliminar directamente o marcar como 'cancelada')
        reserva.delete()

        return JsonResponse({"mensaje": "Reserva cancelada exitosamente"}, status=200)

    # Si el método HTTP no es DELETE
    return JsonResponse({"error": "Método no permitido. Use DELETE para esta acción."}, status=405)




def listar_comentarios(request, evento_id):

    # Parámetros de filtrado y paginación desde los argumentos de la URL o la solicitud
    usuario = request.GET.get("usuario", "")  # Filtrar por usuario (username)
    orden = request.GET.get("orden", "-fecha_creacion")  # Ordenar por fecha de creación (más reciente por defecto)
    limite = int(request.GET.get("limite", 5))  # Límite de comentarios por página
    pagina = int(request.GET.get("pagina", 1))  # Número de página actual

    # Verificar si el evento existe
    try:
        evento = Evento.objects.get(id=evento_id)
    except Evento.DoesNotExist:
        return JsonResponse({"error": "El evento especificado no existe."}, status=404)

    # Filtrar comentarios asociados al evento
    comentarios = Comentario.objects.filter(evento=evento).select_related("usuario")

    # Filtrar por usuario, si se proporciona
    if usuario:
        comentarios = comentarios.filter(usuario__username__icontains=usuario)

    # Aplicar orden
    comentarios = comentarios.order_by(orden)

    # Paginación
    paginator = Paginator(comentarios, limite)

    try:
        comentarios_pagina = paginator.page(pagina)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    # Formatear respuesta con datos paginados
    data = {
        "count": paginator.count,  # Número total de comentarios
        "total_pages": paginator.num_pages,  # Total de páginas
        "current_page": pagina,  # Página actual
        "next": pagina + 1 if comentarios_pagina.has_next() else None,  # Página siguiente (si existe)
        "previous": pagina - 1 if comentarios_pagina.has_previous() else None,  # Página anterior (si existe)
        "results": [
            {
                "id": comentario.id,
                "usuario": comentario.usuario.username,
                "texto": comentario.texto,
                "fecha_creacion": comentario.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
            }
            for comentario in comentarios_pagina
        ]
    }

    return JsonResponse(data, safe=False)



@csrf_exempt
def crear_comentario(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Usa POST.'}, status=405)

    try:
        # Parsear el JSON enviado en la solicitud
        datos = json.loads(request.body.decode('utf-8'))

        # Obtener los campos enviados desde el cliente
        texto = datos.get('texto')
        evento_id = datos.get('evento')
        usuario_id = datos.get('usuario')

        # Validar que se envían los campos obligatorios
        if not texto or not evento_id or not usuario_id:
            return JsonResponse({'error': 'Los campos "texto", "evento" y "usuario" son obligatorios.'}, status=400)

        # Validar que "usuario_id" sea un número entero
        try:
            usuario_id = int(usuario_id)  # Convertir a número entero
        except (ValueError, TypeError):
            return JsonResponse({'error': '"usuario" debe ser un número válido (un id numérico).'}, status=400)

        # Verificar si el usuario existe
        try:
            usuario_actual = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'El usuario especificado no existe.'}, status=404)

        # Verificar si el evento existe
        try:
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist:
            return JsonResponse({'error': 'El evento especificado no existe.'}, status=404)

        # Crear el comentario
        comentario = Comentario.objects.create(
            texto=texto,
            usuario=usuario_actual,
            evento=evento
        )

        # Responder con éxito y los detalles del comentario creado
        return JsonResponse({
            'mensaje': 'Comentario creado exitosamente.',
            'comentario': {
                'id': comentario.id,
                'texto': comentario.texto,
                'fecha_creacion': comentario.fecha_creacion.isoformat(),
                'usuario': {
                    'id': usuario_actual.id,
                    'username': usuario_actual.username
                },
                'evento': {
                    'id': evento.id
                }
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato de JSON inválido.'}, status=400)
    except Exception as e:
        # Captura cualquier otro error y lo muestra
        return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)


@csrf_exempt
def login_usuario(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Usa POST.'}, status=405)

    try:
        # Parsear el JSON enviado en la solicitud
        datos = json.loads(request.body.decode('utf-8'))

        # Obtener username y password del JSON
        username = datos.get('username')
        password = datos.get('password')

        # Validar que ambos campos sean proporcionados
        if not username or not password:
            return JsonResponse({'error': 'Los campos "username" y "password" son obligatorios.'}, status=400)

        # Verificar si el usuario existe
        try:
            usuario = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Credenciales inválidas. Usuario no encontrado.'}, status=401)

        # Si las credenciales son correctas, devolver datos del usuario
        return JsonResponse({
            'mensaje': 'Inicio de sesión exitoso.',
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'rol': usuario.rol,  # Este es tu campo personalizado en el modelo
            }
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato de JSON inválido.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)




@csrf_exempt
def registrar_usuario(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Usa POST.'}, status=405)

    try:
        # Parsear el JSON enviado en la solicitud
        datos = json.loads(request.body.decode('utf-8'))

        # Obtener los datos enviados en el JSON
        username = datos.get('username')
        password = datos.get('password')
        rol = datos.get('rol', 'participante')  # Valor predeterminado: 'participante'
        biografia = datos.get('biografia', '')

        # Validar que los campos obligatorios estén presentes
        if not username or not password:
            return JsonResponse({'error': 'Los campos "username" y "password" son obligatorios.'}, status=400)

        # Convertir la contraseña en cadena y validarla
        if not str(password).isdigit():
            return JsonResponse({'error': 'La contraseña debe contener únicamente números.'}, status=400)

        # Verificar si el usuario ya existe en la base de datos
        if Usuario.objects.filter(username=username).exists():
            return JsonResponse({'error': 'El username ya está en uso. Elige otro.'}, status=409)

        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            username=username,
            rol=rol,
            biografia=biografia
        )

        # Definir la contraseña correctamente utilizando set_password
        nuevo_usuario.set_password(str(password))  # Convertir la contraseña a cadena antes de encriptar
        nuevo_usuario.save()

        # Responder con éxito y detalles del usuario recién creado
        return JsonResponse({
            'mensaje': 'Usuario registrado exitosamente.',
            'usuario': {
                'id': nuevo_usuario.id,
                'username': nuevo_usuario.username,
                'rol': nuevo_usuario.rol,  # Campo personalizado
                'biografia': nuevo_usuario.biografia
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato de JSON inválido.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)

































































from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .logic import generar_reporte, consultar_reporte, eliminar_reporte
import json
import requests

@csrf_exempt
def generar_reporte_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigo = data.get('codigo')
        estudiante = data.get('estudiante') #numId del estudiante
        emisor = data.get('emisor')
        if check_estudiante(estudiante) != None:
            reporte = generar_reporte(codigo, estudiante, emisor)
            return JsonResponse({'codigo': reporte.codigo, 'estudiante': reporte.estudiante, 'fechaEmision': reporte.fechaEmision, 'emisor': reporte.emisor})

@csrf_exempt
def consultar_reporte_view(request, codigo):
    if request.method == 'GET':
        # Primero, obtenemos el reporte usando el código
        reporte = consultar_reporte(codigo)
        
        if reporte:
            try:
                # Obtenemos la información del estudiante usando la función check_estudiante
                estudiante = check_estudiante(reporte.estudiante)
                
                # Embebemos la información del estudiante en la respuesta JSON del reporte
                return JsonResponse({
                    'codigo': reporte.codigo,
                    'estudiante': estudiante,  # Aquí agregamos el objeto estudiante completo
                    'fechaEmision': reporte.fechaEmision,
                    'emisor': reporte.emisor
                })
            except ValueError as e:
                # Si ocurre un error al obtener el estudiante, respondemos con el error
                return JsonResponse({'error': str(e)}, status=400)
        else:
            # Si el reporte no se encuentra, respondemos con un error
            return JsonResponse({'error': 'Reporte no encontrado'}, status=404)


@csrf_exempt
def eliminar_reporte_view(request, codigo):
    if request.method == 'DELETE':
        eliminado = eliminar_reporte(codigo)
        if eliminado:
            return JsonResponse({'mensaje': 'Reporte eliminado correctamente'})
        else:
            return JsonResponse({'error': 'Reporte no encontrado'}, status=404)


@csrf_exempt
def check_estudiante(idEstudiante):
    """Obtiene el estudiante de la otra máquina usando el idEstudiante"""
    try:
        path = f"http://34.41.63.193:8080/students/{idEstudiante}"  # Cambiar IP si es necesario
        r = requests.get(path, headers={"Accept": "application/json"})
        r.raise_for_status()  # Lanza una excepción si la respuesta es un error (4xx, 5xx)

        # Si la respuesta es exitosa, procesamos la respuesta JSON
        estudiante = r.json()
        return estudiante

    except requests.exceptions.HTTPError as http_err:
        # Capturamos errores específicos de HTTP (como 404, 500, etc.)
        if r.status_code == 404:
            raise ValueError(f"Estudiante con ID {idEstudiante} no encontrado.")
        else:
            raise ValueError(f"Error HTTP al obtener el estudiante: {http_err}")
    
    except requests.exceptions.RequestException as req_err:
        # Capturamos errores generales de la solicitud (como problemas de red, conexión rechazada, etc.)
        raise ValueError(f"Error en la solicitud de red: {req_err}")
    
    except Exception as e:
        # Capturamos cualquier otro tipo de error inesperado
        raise ValueError(f"Ocurrió un error inesperado: {e}")

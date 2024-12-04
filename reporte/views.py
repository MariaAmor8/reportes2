from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .logic import generar_reporte, consultar_reporte, eliminar_reporte
import json

@csrf_exempt
def generar_reporte_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigo = data.get('codigo')
        estudiante = data.get('estudiante')
        emisor = data.get('emisor')
        reporte = generar_reporte(codigo, estudiante, emisor)
        return JsonResponse({'codigo': reporte.codigo, 'estudiante': reporte.estudiante, 'fechaEmision': reporte.fechaEmision, 'emisor': reporte.emisor})

@csrf_exempt
def consultar_reporte_view(request, codigo):
    if request.method == 'GET':
        reporte = consultar_reporte(codigo)
        if reporte:
            return JsonResponse({'codigo': reporte.codigo, 'estudiante': reporte.estudiante, 'fechaEmision': reporte.fechaEmision, 'emisor': reporte.emisor})
        else:
            return JsonResponse({'error': 'Reporte no encontrado'}, status=404)

@csrf_exempt
def eliminar_reporte_view(request, codigo):
    if request.method == 'DELETE':
        eliminado = eliminar_reporte(codigo)
        if eliminado:
            return JsonResponse({'mensaje': 'Reporte eliminado correctamente'})
        else:
            return JsonResponse({'error': 'Reporte no encontrado'}, status=404)
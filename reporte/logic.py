from .models import Reporte

def generar_reporte(codigo, estudiante, emisor):
    """
    Genera un nuevo reporte y lo guarda en la base de datos.
    
    :param codigo: código del reporte
    :param estudiante: identificador del estudiante
    :param emisor: nombre del emisor
    :return: reporte generado
    """
    reporte = Reporte.objects.create(codigo=codigo, estudiante=estudiante, emisor=emisor)
    return reporte

def consultar_reporte(codigo):
    """
    Consulta un reporte dado su código.
    
    :param codigo: código del reporte
    :return: reporte correspondiente al código, o None si no existe
    """
    try:
        reporte = Reporte.objects.get(codigo=codigo)
        return reporte
    except Reporte.DoesNotExist:
        return None

def eliminar_reporte(codigo):
    """
    Elimina un reporte dado su código.
    
    :param codigo: código del reporte
    :return: True si se eliminó el reporte, False si no existe
    """
    try:
        reporte = Reporte.objects.get(codigo=codigo)
        reporte.delete()
        return True
    except Reporte.DoesNotExist:
        return False

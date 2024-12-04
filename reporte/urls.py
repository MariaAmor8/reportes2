from django.urls import path
from . import views

urlpatterns = [
    path('reporte/', views.generar_reporte_view, name='generar_reporte'),
    path('reporte/<int:codigo>/', views.consultar_reporte_view, name='consultar_reporte'),
    path('reporte/<int:codigo>/', views.eliminar_reporte_view, name='eliminar_reporte'),
]

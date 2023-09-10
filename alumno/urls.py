from django.urls import path
from . import views

app_name = 'alumno'

urlpatterns = [
    path('', views.seleccion_materias, name = 'seleccion_materias'),
    path('obtenerMateriasJson/<int:id>', views.obtener_materias, name = 'obtener_materias'),
    path('cursarMaterias/', views.cursar_materias, name = 'cursar_materias'),
    path('dejarMaterias/', views.dejar_materias, name = 'dejar_materias'),
    path('verMaterias/', views.ver_materias, name = 'ver_materias'),
    path('obtenerMateriasConCorrelativas/<int:id>', views.obtener_materias_con_correlativas, name = 'obtener_materias_con_correlativas'),
    path('verNotas/<int:id>', views.ver_notas, name = 'ver_notas'),
    path('obtenerNotas/<int:id>', views.obtener_notas, name = 'obtener_notas'),
    path('obtenerObservacion/<int:id>', views.obtener_observacion, name = 'obtener_observacion'),
    
]
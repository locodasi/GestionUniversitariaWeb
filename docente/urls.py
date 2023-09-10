from django.urls import path
from . import views

app_name = 'docente'

urlpatterns = [
    path('', views.ver_alumnos, name = 'ver_alumnos'),    
    path('obtenerAlumnosDeMateria/<int:id>', views.obtenerAlumnosDeMateria, name = 'obtenerAlumnosDeMateria'),   
    path('obtenerMateriasDeCarrera/<int:id>', views.obtenerMateriasDeCarrera, name = 'obtenerMateriasDeCarrera'),    
    path('notas/<int:idMateria>/<int:idAlumno>', views.notas, name = 'notas'), 
    path('notas/obtenerNotas/<int:idAlumno>/<int:idMateria>', views.obtenerNotas, name = 'obtenerNotas'),    
    path('notas/obtenerNotaJson/<int:id>', views.obtenerNota, name = 'obtenerNota'),   
    path('notas/eliminarNota', views.eliminarNota, name = 'eliminarNota'),   
    path('notas/aprobar/<int:idMateria>/<int:idAlumno>', views.aprobar, name = 'aprobar'),    
]
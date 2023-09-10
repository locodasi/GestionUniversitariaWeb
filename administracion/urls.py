
from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    path('crearCarrera', views.crearCarrera, name = 'crearCarrera'),
    path('obtenerCarreras/', views.obtenerCarreras, name='obtenerCarreras'),
    path('obtenerIdCarrerasSegunAlumno/<int:id>', views.obtenerIdCarrerasSegunAlumno, name='obtenerIdCarrerasSegunAlumno'),
    path('eliminarCarrera', views.eliminarCarrera, name = 'eliminarCarrera'),
    path('crearDocente', views.crearDocente, name = 'crearDocente'),
    path('obtenerDocentes/', views.obtenerDocentes, name='obtenerDocentes'),
    path('eliminarDocente', views.eliminarDocente, name = 'eliminarDocente'),
    path('crearAlumno', views.crearAlumno, name = 'crearAlumno'),
    path('obtenerAlumnos/', views.obtenerAlumnos, name='obtenerAlumnos'),
    path('eliminarAlumno', views.eliminarAlumno, name = 'eliminarAlumno'),
    path('crearMateria', views.crearMateria, name = 'crearMateria'),
    path('obtenerMaterias/', views.obtenerMaterias, name='obtenerMaterias'),
    path('eliminarMateria', views.eliminarMateria, name = 'eliminarMateria'),
    path('correlativas/', views.correlativas, name = 'correlativas'),
    path('obtenerCorrelativas/<str:id>', views.obtenerCorrelativas, name = 'obtenerCorrelativas'),
    path('guardarCorrelativas/', views.guardarCorrelativas, name = 'guardarCorrelativas'),
    path('obtenerIdCarreraDocenteSegunMateria/<int:id>', views.obtenerIdCarreraDocenteSegunMateria, name='obtenerIdCarreraDocenteSegunMateria'),
    path('error/<str:error>', views.error, name = 'error'),
    path('alumnosCursando/<str:dato>', views.alumnosCursando, name = 'alumnosCursando'),
    path('obtenerAlumnos/carrera/<str:id>', views.obtenerAlumnosSegunCarrera, name = 'obtenerAlumnosSegunCarrera'),
    path('obtenerAlumnos/materia/<str:id>', views.obtenerAlumnosSegunMateria, name = 'obtenerAlumnosSegunMateria'),
    
]
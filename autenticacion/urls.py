from django.urls import path
from . import views

app_name = 'autenticacion'

urlpatterns = [
    path('', views.iniciar_sesion, name = 'iniciar_sesion'),
    path('cerrar_sesion', views.cerrar_sesion, name = 'cerrar_sesion'),
    path('cambiar_contraseña', views.cambiar_contraseña, name = 'cambiar_contraseña'),
    
]
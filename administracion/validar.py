from.models import CustomUser, Carrera,Materia
from datetime import datetime, timedelta

import re


def tieneLetra(text):
    for letra in text:
        if letra.isalpha():
            return True
    
    return False
        

def validarCarrera(carrera:Carrera):
    errores = []
    if len(carrera.nombre) < 3 or len(carrera.nombre) > 50:
        errores.append("El nombre debe tener entre 3 y 50 caracteres")
    
    if not tieneLetra(carrera.nombre):
        errores.append("El nombre debe contener al menos una letra")
    
    if type(carrera.duracion) != float:
        errores.append("La duracion debe contener unicamente numeros")
    else:
        
        #Es dentro de un else para asegurarme que sea float
        if carrera.duracion <= 0 or carrera.duracion > 12:
            errores.append("La duracion debe ser mayor a 0 y menor o igual a 12")
        
        if len(str(carrera.duracion).split(".")[1]) > 2:
             errores.append("Solo puede haber 2 numeros despues de la coma")
    
    return errores

def validarUsuario(docente:CustomUser):
    errores = []
    #Valido que nombre y apellido no tenga numero
    if not docente.first_name.replace(" ","").isalpha():
        errores.append("El nombre solo pueden ser letras")
    
    if len(docente.first_name) < 3 or len(docente.first_name) > 50:
        errores.append("El nombre debe contener entre 3 y 50 caracteres")
    
    if not docente.last_name.replace(" ","").isalpha():
        errores.append("El apellido solo pueden ser letras")
    
    if len(docente.last_name) < 3 or len(docente.last_name) > 50:
        errores.append("El apellido debe contener entre 3 y 50 caracteres")
    
    #Me aseguro que sea numerica y de longitud 8
    if not docente.username.isnumeric() or len(docente.username)!= 8:
        errores.append("El DNI debe ser entre 10000000 y 99999999")
    
    patron = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}"
    if not re.match(patron,docente.email):
        errores.append("El email es invalido")
            
    
    return errores

def validarDocente(user):
    return validarUsuario(user)

def es_arreglo_numerico(arr, arr_de_existentes):
    for elemento in arr:
        try:
            #Esto porque los datos pasados por el form estan en str, asi que primero si no es un str, alguien me hackeo y fuera y si lo es despues valido que sea un numero
            if type(elemento) != str:
                return False
            int(elemento)
        except:
            return False
        
    for elemento in arr:
        elemento = int(elemento)
        if not elemento in arr_de_existentes:
            return False
        
    return True

def validarAlumno(user, id_carreras_elegidas, id_carreras_existentes):
    errores = validarUsuario(user)
    
    if len(id_carreras_elegidas) == 0 or not es_arreglo_numerico(id_carreras_elegidas, id_carreras_existentes):
        errores.append("Ingrese una o mas carreras validas")
        
    return errores

def validarMateria(materia:Materia):
    errores = []
    if Carrera.objects.filter(id=materia.carrera_id) == 1:
        errores.append("Elija una carrera valida")
    
    if len(materia.nombre) < 3 or len(materia.nombre) > 50 or not tieneLetra(materia.nombre):
        errores.append("El nombre debe contener entre 3 y 50 caracteres y contener letras")
    
    dias_de_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    if not materia.dia in dias_de_semana:
        errores.append("Elija una dia valido")
        
    if materia.hasta <= materia.desde:
        errores.append("Desde no puede ser mayor a hasta")
    else:    
        tiempo_diferencia = datetime.combine(datetime.min, materia.hasta) - datetime.combine(datetime.min, materia.desde)
        
        if tiempo_diferencia < timedelta(minutes=40):
            errores.append("El intervalo de tiempo no puede ser menor a 40 minutos")
        
    if CustomUser.objects.filter(id=materia.docente_id, grupo="Docente") == 1:
        errores.append("Elija un docente valido")
    
    return errores

    
        
    
    

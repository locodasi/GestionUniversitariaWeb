from administracion.models import Carrera,Materia,Alumno_Materia,CustomUser,Nota
from alumno.excepcion import MiExcepcion
from datetime import datetime
import calendar

def obtenerCarrerasDeDocente(idDocente):
    # Esta consulta retorna una lista de nombres de carreras distintas
    # que cumplen con las condiciones dadas en la consulta SQL original.
    carreras_distintas = Carrera.objects.filter(
        materia__docente_id=idDocente,  # Hace referencia a la relación con la tabla Materia
        actual=1,  # Condición de actual en la tabla Carrera
        materia__actual=1  # Condición de actual en la tabla Materia
    ).distinct().values_list('id', 'nombre')

    # El resultado es una lista de nombres de carreras distintas
    
    return carreras_distintas

#Si lanza algun error, no esta validado, si no lo hace, si 
def validarMateriaDeDocente(idMateria,idDocente):
    try:
        Materia.objects.get(id=idMateria,docente_id=idDocente,actual=True)
    except:
        raise MiExcepcion("La materia o no existe, o no es actual o no esta a cargo de este docente")

#Funcion que retorna a los alumnos serializadso de mi materia
def obtenerAlumnosDeMateriaDocente(idMateria,idDocente):
    validarMateriaDeDocente(idMateria=idMateria,idDocente=idDocente)
    alumnos_materias = Alumno_Materia.objects.filter(materia_id=idMateria,estado="Cursando")
    
    alumnosSerializados = []
    
    for alumno_materia in alumnos_materias:
        alumnosSerializados.append(serilizarAlumno(alumno_materia.estudiante))
    
    return alumnosSerializados

def serilizarAlumno(alumno:CustomUser):
    objetoSerializado = {
        "id":alumno.id,
        "nombre": alumno.first_name,
        "apellido": alumno.last_name,
        "dni": alumno.username,
        "email": alumno.email,
    }
    
    return objetoSerializado

def valdarCarreraExistente(idCarrera):    
    try:
        Carrera.objects.get(id=idCarrera,actual=True)
    except:
        raise MiExcepcion("La carrera no es actual o no existe")

def obtenerMateriasDeCarreraDocente(idCarrera,idDocente):
    valdarCarreraExistente(idCarrera)
    materias = Materia.objects.filter(carrera_id=idCarrera,docente_id=idDocente,actual=True).values_list("id","nombre")
    
    materiasSerializadas = []
    for materia in materias:
        materiasSerializadas.append({"id":materia[0],"nombre":materia[1]})
    
    return materiasSerializadas

def obtenerTiposNotas():
    tipos = ["TP","Parcial","Final","Exposicion","Tesis", "Exposicion grupal"]
    
    return tipos

def validarQueIdDeNotaEsDeMiDocente(id,idDocente):
    nota = Nota.objects.get(id=id)
    if nota.materia.docente.id != idDocente:
        raise MiExcepcion("Nota inexistente o no perteneciente a este docente")
    
def validarNota(nota:Nota):
    errores = []
    notaRedondeada = 0
    try:
        notaRedondeada = round(float(nota.nota), 2)
    except Exception as e:
        print(e)
        errores.append("Nota invalida")
    
    if notaRedondeada < 1 or notaRedondeada > 10:
        errores.append("La nota debe estar entre 1 y 10")
    
    if not nota.tipo in obtenerTiposNotas():
        errores.append("Tipo invalido")
    
    valor, error = validarFecha(nota.dia)
    if valor:
        errores.append(error)
    
    return errores

def validarFecha(fecha):
    if not FechaValida(fecha):
        return  True, "Fecha invalida"
    if fechaPosterior(fecha):
        return True,"La fecha no puede ser posterior a hoy"
    return False, None
        
def fechaPosterior(fecha):
    try:

        # Obtiene la fecha actual
        fecha_actual = datetime.now()

        # Compara las fechas
        if fecha > fecha_actual:
            return True
        
        #No pueden haber notas de antes del 2000
        if fecha.year < 2000:
            return True
        
        return False

    except ValueError:
        # Maneja el caso en el que la cadena de fecha no sea válida
        return True
    

def FechaValida(fecha):
    try:

        # Verifica si la fecha es válida en el calendario
        año = fecha.year
        mes = fecha.month
        dia = fecha.day

        if año < 1 or año > 9999 or mes < 1 or mes > 12 or dia < 1 or dia > calendar.monthrange(año, mes)[1]:
            return False

        return True
    except:
        # Maneja el caso en el que la cadena de fecha no sea válida
        return False
    
def pasarFechaAString(fecha):
    #Si fecha es none, osea invalida para ser un dato date, devuelvo none
    if fecha == None:
        return None
    año = fecha.year
    mes = fecha.month
    dia = fecha.day
    
    #Estosif son para que mes y dia siempre tengan 2 numeros
    if mes < 10:
        mes = f"0{mes}"    
    
    if dia < 10:
        dia = f"0{dia}"
    
    return f"{año}-{mes}-{dia}"

def modificarObservacion(observacion):
    posicion = observacion.find("\n")
    if posicion == -1:
        return observacion[:30] + "..." if len(observacion) > 30 else observacion
    else:
        return observacion[:posicion] + "..."
    
    
    
    
    

from administracion.models import CustomUser, Alumno_Materia,Correlativa,Materia, Alumno_Carrera
from django.shortcuts import get_object_or_404
from .excepcion import MiExcepcion
from email.message import EmailMessage
import smtplib
import threading

def formatoConCeros(id,cantNumeros):
    idtring = str(id)
    cantNumeros -= len(idtring)
    
    return "0" * cantNumeros + idtring

#Si no esta lanza un error, si esta, no hace nada
def validarAlumnoEnCarrera(idCarrera, idAlumno):
    try:        
        Alumno_Carrera.objects.get(estudiante_id=idAlumno,carrera_id=idCarrera,carrera__actual=True)
    except:
        raise MiExcepcion("El alumno no pertenece a esta carrera o el alumno o carrera no existe") 
    

def validarCorrelativas(materia, idAlumno):
    #Traigo las correlativas de la materia
    correlativas = Correlativa.objects.filter(materia_id=materia.id)
            
    #Si no tiene correlativas se puede sumar, si no, no
    if len(correlativas) == 0:                   
        return True
    #Hacer esat consulta como las otras estaba siendo muy dificil asi que la escribi en sql, los %s son variables, esta consulta me da aquellos alumnos_materias de mi alumno y que sean correlativas de la materia y que esten aprobadas, por lo que esta consulta retorna todas las correlativas de la materia que tenga aprobada
    query = f"""select *
        from administracion_alumno_materia am inner join administracion_correlativa co on co.correlativa_id = am.materia_id
        where am.estudiante_id = %s and co.materia_id = %s and am.estado = 'Aprobado'"""

    parametros = [idAlumno, materia.id]

    #Con raw se hace el coso, pero si queres ver correlativasAprobadas, solo vas a ver la consulta, no el resultado, para eso tenes que iterar
    correlativasAprobadas = Alumno_Materia.objects.raw(query, parametros)

    #Si la lista de correlativas es igual a la de aprobadas, significa que hice todo, por lo que la pueda dar como opcion de cursada, si no, no
    if len(correlativasAprobadas) == len(correlativas):
        return True
    else:
        return False
    
def obtenerMaterias(idCarrera, idAlumno):
    listaMaterias = []
    listaCursando = []
    listaAprobada = []
    
    #Si el alumno no esta en la carrera o no existe lanza un error, que atrapara js para recargar la pagina
    validarAlumnoEnCarrera(idCarrera=idCarrera,idAlumno=idAlumno)
        
            
    #Obtengo todas las materias de la carrera
    materiasDeLaCarrera = Materia.objects.filter(carrera_id=idCarrera, actual=True)
        
    for materia in materiasDeLaCarrera:
        #Obtengo de cada materia su estado de alumno_materia, si no existe porque nunca la curso, da vacio
        alumno_materia = Alumno_Materia.objects.filter(estudiante_id = idAlumno,materia_id = materia.id)
        
        #Si se curso o se aprobo se agrega a su respectiva lista, si esta vacio le hago mas cosas para ver si no tiene correlativas para agregarlo a la lista de materias para cursar
        if len(alumno_materia) == 0:
            if validarCorrelativas(idAlumno=idAlumno,materia=materia):
                listaMaterias.append([materia.id , f"{formatoConCeros(materia.id,5)} {materia.nombre}"])                     
            
        elif alumno_materia[0].estado == "Cursando":
            listaCursando.append([materia.id , f"{formatoConCeros(materia.id,5)} {materia.nombre}"])
            
        elif alumno_materia[0].estado == "Aprobado":
            listaAprobada.append([materia.id , f"{formatoConCeros(materia.id,5)} {materia.nombre}"])
            
    return listaMaterias, listaCursando, listaAprobada

def validarMateriaParaCursar(idMateria,idUsuario,idCarrera):
    materia = get_object_or_404(Materia,id=idMateria)
    
    #Validar que la carrera pertenezca a la carrera
    if materia.carrera.id != idCarrera:
        raise MiExcepcion("La materia no pertenece a esta carrera")
    
    #Valido si el usario pertenece a esta carrera
    validarAlumnoEnCarrera(idCarrera=materia.carrera.id,idAlumno=idUsuario)
    
    #Valido si el alumno ya la esta cursando o la aprobo
    alumno_materia = Alumno_Materia.objects.filter(estudiante_id = idUsuario,materia_id = materia.id)
    
    if len(alumno_materia) != 0:
        raise MiExcepcion("El alumno ya esta cursando o tiene aprobada la materia")
    
    #valido si puede cursarla segun las correlativas
    if not validarCorrelativas(idAlumno=idUsuario,materia=materia):
        raise MiExcepcion("El alumno no cumple con las correlativas")
    
    #Supero todas las validaciones, el alumno la puede cursar
    return True

def validarMateriaParaDejar(idMateria,idUsuario,idCarrera):
    materia = get_object_or_404(Materia,id=idMateria)
    
    #Validar que la carrera pertenezca a la carrera
    if materia.carrera.id != idCarrera:
        raise MiExcepcion("La materia no pertenece a esta carrera")
    
    try:
        Alumno_Materia.objects.get(estudiante_id = idUsuario,materia_id = materia.id, estado="Cursando")
    except:
        raise MiExcepcion("El alumno no esta cursando esta materia o carrera o ya la tiene aprobada")
    
    #Supero todas las validaciones, el alumno la puede cursar
    return True


def agregarCursada(idsMaterias,idAlumno):
    cargarCursada(idsMaterias=idsMaterias,idAlumno=idAlumno)
    enviarEmaildeMaterias(idsMaterias=idsMaterias,idAlumno=idAlumno)

def dejarCursada(idsMaterias,idAlumno):
    cargarAbandono(idsMaterias=idsMaterias,idAlumno=idAlumno)
    enviarEmaildeMaterias(idsMaterias=idsMaterias,idAlumno=idAlumno,cursar=False)

#Cargo a la base de datos
def cargarCursada(idsMaterias,idAlumno):
    try:
        #Creo una lista con todos los alumno_materia que voy a crear, este es un for en una sola linea, podria haberlo hecho como un for normal, y al poner el for directo entre [] ya esta poniendo los alumno_materia dentro de la lista
        alumnos_materias = [Alumno_Materia(estudiante_id=idAlumno, materia_id=idMateria) for idMateria in idsMaterias]

        #Con bulk_create creo varios insert de una lista de Alumno_Materia
        Alumno_Materia.objects.bulk_create(alumnos_materias)
    except Exception as e:
        print(e)
        
#Elimino de la base de datos
def cargarAbandono(idsMaterias,idAlumno):
    try:
        #materia_id__in, esto es como hacer un materia_id in ... en sql, asi en una sola consulta puedo obtener todas las alumno_materia y borrarlas
        alumnos_materias = Alumno_Materia.objects.filter(estudiante_id=idAlumno, materia_id__in=idsMaterias,estado="Cursando")
        alumnos_materias.delete()
    except Exception as e:
        print(e)
        
def enviarEmaildeMaterias(idsMaterias,idAlumno,cursar=True):
    alumno = get_object_or_404(CustomUser,id=idAlumno) 
    asunto = ""
    mensaje = ""
    if cursar:
        mensaje, asunto = crearMensajeCursar(idsMaterias=idsMaterias,alumno=alumno)
    else:
        mensaje, asunto = crearMensajeDejar(idsMaterias=idsMaterias,alumno=alumno)
    
    email = creacionDeMail(destinatario=alumno.email,asunto=asunto,mensaje=mensaje)
        
    try:
        #Enviar email como hilo, ahora va a fallar porque no tiene un mail remitente valido
        #Siempre pasar los args como una tupla
        hiloDeMail = threading.Thread(target=envioEmail, args=(email,))
        hiloDeMail.start()
    except Exception as e:
        print(e)

def crearMensajeCursar(idsMaterias,alumno):
    mensaje = ""
    carrera = Materia.objects.get(id=idsMaterias[0]).carrera  

    if len(idsMaterias) == 1:
        materia = Materia.objects.get(id=idsMaterias[0])           
        mensaje += f"""Hola {alumno.first_name} {alumno.last_name}, fuiste correctamente inscripto en la materia de {materia.nombre} de la carrera de {carrera.nombre}.
    
    
        ATT.
            La direccion"""
    else:
        mensaje = f"Hola {alumno.first_name} {alumno.last_name}, fuiste correctamente inscripto a las materias de "
            
        for idMateria in idsMaterias:
            materia = Materia.objects.get(id=idMateria) 
            mensaje += f"{materia.nombre}, "
            
        #Para borrar la ultima coma
        mensaje = mensaje[:len(mensaje)-1]
            
        mensaje += f""" de la carrera de {carrera.nombre}.
        
        
        ATT.
            La direccion"""
                
    return mensaje, "Inscripcion a materias"

def crearMensajeDejar(idsMaterias,alumno):
    mensaje = ""
    carrera = Materia.objects.get(id=idsMaterias[0]).carrera  

    if len(idsMaterias) == 1:
        materia = Materia.objects.get(id=idsMaterias[0])           
        mensaje += f"""Hola {alumno.first_name} {alumno.last_name}, abandonaste correctamente la materia de {materia.nombre} de la carrera de {carrera.nombre}.
    
    
        ATT.
            La direccion"""
    else:
        mensaje = f"Hola {alumno.first_name} {alumno.last_name}, abandonaste correctamente las materias de "
            
        for idMateria in idsMaterias:
            materia = Materia.objects.get(id=idMateria) 
            mensaje += f"{materia.nombre}, "
            
        #Para borrar la ultima coma
        mensaje = mensaje[:len(mensaje)-1]
            
        mensaje += f""" de la carrera de {carrera.nombre}.
        
        
        ATT.
            La direccion"""
                
    return mensaje, "Abandono de materias"

def creacionDeMail(destinatario,asunto,mensaje):
    #Podes poner tanto homtial,como gmail, etc
    email = EmailMessage()
    email["From"] = "emial@hotmail.com"
    email["To"] = destinatario
    email["Subject"] = asunto
    email.set_content(mensaje)
    
    return email

def envioEmail(email:EmailMessage):
    #Aca depende que servidor use el remitente del mail, gmail, hotmail,etc, este es para hotmail
    #lo mismo con el puerto, dependera que uses
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(email["From"], "tuContra")
    smtp.sendmail(email["From"], email["To"], email.as_string())
    smtp.quit()

#Funcion que retorna un dict en base a materia de esta forma
# {
#     "idMateria": "1",
#     "nombreMateria": "juan",
#     "correlativasMateria": "(1,3,43,3)"
# }
def crearMateriaConCorrelativas(materia:Materia):
    #Primero busco a quellas que sean correlativas a materia y que sean actuales, ya que la actual tiene que ser correlativa_id y no materia, hago correlativa__actual en vez de materia, luego pido en version de lista el valor correlativa_id, y para que no me haga listas anidadas, osea cada respuesta es una lista, osea si 12 es correlativa 2 y 3 no me haga (2,),(3,) que me haga (2,3), hago flat=true, luego lo meto en una tupla para que directamente pueda pasarlo astring (2,3)
    materiasCorrelativas = tuple(Correlativa.objects.filter(materia_id=materia.id,correlativa__actual=True).values_list("correlativa_id", flat=True))
        
    #La convierto en un string, si no tiene nada es nada, si tiene uno lo hago asi para que no quede 2,, ya que si una tupla tiene un solo dato lo hace asi, y si tiene mas lo deja normal
    correlativas = ""
    if len(materiasCorrelativas) == 1:
        correlativas = f"({materiasCorrelativas[0]})"
    elif len(materiasCorrelativas) > 1:     
        correlativas = f"{materiasCorrelativas}"
    
    materiaSerilaizada ={
        "idMateria": materia.id,
        "nombreMateria": materia.nombre,
        "correlativasMateria": correlativas
    }
    
    return materiaSerilaizada

def modificarObservacion(observacion):
    posicion = observacion.find("\n")
    if posicion == -1:
        return observacion[:30] + "..." if len(observacion) > 30 else observacion
    else:
        return observacion[:posicion] + "..."
    
    
    
    
    
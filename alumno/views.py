from django.shortcuts import render,redirect,get_object_or_404
from administracion.models import Alumno_Carrera,Materia,Alumno_Materia,Nota
from django.contrib.auth.decorators import login_required, user_passes_test
from .ayudas import obtenerMaterias,validarMateriaParaCursar,agregarCursada,validarMateriaParaDejar,dejarCursada,validarAlumnoEnCarrera,crearMateriaConCorrelativas,modificarObservacion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json


# Create your views here.

@login_required
@user_passes_test(lambda u: u.grupo == "Alumno", login_url='autenticacion:iniciar_sesion') 
def seleccion_materias(request):
    #En el values la razon por la que uso 1 _ y 2, es porque carrera_id es el valor de l atabla alumno_carrera, pero el nombre es un valor de la tabla carrera, por eso hago doble _, es como para decirle, no de esta tabla (Alumno_Carrera) si no de la que obtengo (carrera)
    #Esto me deja un querySet, que es una lista con un dict con los datos en de value, y las claves de esos datos son los nombre puestos, por loque en el html, cunado haga el for no va a ser carrera.id (porque no es un obj), si no carrera.carera_id, (porque es un dict y esa la clave), en nombre se mantiene los 2 __, osea carrera.carrera__nombre
    carreras = Alumno_Carrera.objects.filter(estudiante_id=request.user.id,estado="Cursando").values('carrera_id', 'carrera__nombre')
    
    #Obtengo las materias de la primera carrera, como base apra la pagina
    listaMaterias,listaCursando,listaAprobada = obtenerMaterias(idCarrera=carreras[0]["carrera_id"],idAlumno=request.user.id)
    
    return render(request,"seleccionMaterias.html",{
        "carreras":carreras,
        "materias": listaMaterias,
        "cursadas": listaCursando,
        "aprobadas": listaAprobada
        })

@login_required
@user_passes_test(lambda u: u.grupo == "Alumno", login_url='autenticacion:iniciar_sesion') 
def obtener_materias(request,id):
    #Obtengo las carreras de este id
    
    listaMaterias,listaCursando,listaAprobada = obtenerMaterias(idCarrera=id,idAlumno=request.user.id)

       
    #Serializo el obj
    materiasSerializadas = {
        "materias":listaMaterias,
        "cursadas":listaCursando,
        "aprobadas":listaAprobada
    }
    
    return JsonResponse(materiasSerializadas, safe=False)

@login_required
@user_passes_test(lambda u: u.grupo == "Alumno", login_url='autenticacion:iniciar_sesion') 
@csrf_protect
def cursar_materias(request):
    if request.method == "POST":
        idUsuario = request.user.id
        obj = json.loads(request.body)
        ids = obj["ids"].split(",")
        idCarrera  = obj["idCarrera"]
        idsMaterias = []
        try:            
            for id in ids:
                validarMateriaParaCursar(idUsuario=idUsuario,idMateria=id, idCarrera=int(idCarrera))
                idsMaterias.append(id)
                    
            agregarCursada(idsMaterias=idsMaterias,idAlumno=idUsuario)
            response_data = {'mensaje': 'Guardado exitoso'}
            return JsonResponse(response_data,status=201)
        except Exception as e:
                    print(e)
                    return JsonResponse({'error': str(e)}, status=400)
    else:
        return redirect("alumno:seleccion_materias")
    
@login_required
@user_passes_test(lambda u: u.grupo == "Alumno", login_url='autenticacion:iniciar_sesion') 
@csrf_protect
def dejar_materias(request):
    if request.method == "POST":
        idUsuario = request.user.id
        obj = json.loads(request.body)
        ids = obj["ids"].split(",")
        idCarrera  = obj["idCarrera"]
        idsMaterias = []
        try:
            for id in ids:
            
                validarMateriaParaDejar(idUsuario=idUsuario,idMateria=id, idCarrera=int(idCarrera))
                idsMaterias.append(id)

            dejarCursada(idsMaterias=idsMaterias,idAlumno=idUsuario)
            response_data = {'mensaje': 'Guardado exitoso'}
            return JsonResponse(response_data,status=201)
        except Exception as e:
                print(e)
                #Hacer lo de enviar email de las materias que tengo hasta aca 
                return JsonResponse({'error': str(e)}, status=400)
    else:
        return redirect("alumno:seleccion_materias")

@login_required
@user_passes_test(lambda u: u.grupo == "Alumno", login_url='autenticacion:iniciar_sesion') 
def ver_materias(request):
    carreras = Alumno_Carrera.objects.filter(estudiante_id=request.user.id,estado="Cursando").values('carrera_id', 'carrera__nombre')
    return render(request,"verMaterias.html",{"carreras":carreras})

@login_required
@user_passes_test(lambda u: u.grupo == "Alumno", login_url='autenticacion:iniciar_sesion') 
def obtener_materias_con_correlativas(request,id):
    validarAlumnoEnCarrera(idCarrera=id,idAlumno=request.user.id)
    #Si no da error, osea el alumno pertenece a la carrera continuo, con obtener todas las materias de la carrera
    materias = Materia.objects.filter(carrera_id=id,actual=True)
    
    materiasConCorrelativasSerializadas = []
    
    for materia in materias:
        #Esta funcion me agrega a la lista un dict con idMateria, nombreMateria y correlativasMateria, qu eva a ser un string con los id de las correlativas (1,3,43,2)
        materiasConCorrelativasSerializadas.append(crearMateriaConCorrelativas(materia=materia))
    
    return JsonResponse(materiasConCorrelativasSerializadas, safe=False)

@login_required
@user_passes_test(lambda u: u.grupo == "Alumno", login_url='autenticacion:iniciar_sesion') 
def ver_notas(request,id):
    alumno_materia =  get_object_or_404(Alumno_Materia,materia_id=id,estudiante_id=request.user.id)
    titulo = f"Notas de la materia {alumno_materia.materia.nombre} de la carrera {alumno_materia.materia.carrera.nombre}"
    
    return render(request,"verNotas.html",{"titulo":titulo,"id":id})

@login_required
@user_passes_test(lambda u: u.grupo == "Alumno", login_url='autenticacion:iniciar_sesion') 
def obtener_notas(request,id):
    try:
        notas = Nota.objects.filter(alumno_id=request.user.id,materia_id=id)
        notasSerializadas = []
            
        for nota in notas:
            notaSerializada = {
                "id":nota.id,
                "nota":nota.nota,
                "fecha":nota.dia,
                "tipo":nota.tipo,
                "observacion": modificarObservacion(nota.observacion)
            }
            notasSerializadas.append(notaSerializada)
            
        return JsonResponse(notasSerializadas,safe=False)
    except Exception as e: 
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@user_passes_test(lambda u: u.grupo == "Alumno", login_url='autenticacion:iniciar_sesion') 
def obtener_observacion(request,id):
    nota = get_object_or_404(Nota,id=id,alumno_id=request.user.id)
    return JsonResponse(f"{nota.observacion}",safe=False)

    
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from administracion.models import Materia,Alumno_Materia,Nota,CustomUser
from .ayudas import obtenerCarrerasDeDocente,obtenerAlumnosDeMateriaDocente,obtenerMateriasDeCarreraDocente,obtenerTiposNotas,validarQueIdDeNotaEsDeMiDocente,validarNota,pasarFechaAString,modificarObservacion
from django.http import JsonResponse
import datetime

# Create your views here.
@login_required
@user_passes_test(lambda u: u.grupo == "Docente", login_url='autenticacion:iniciar_sesion') 
def ver_alumnos(request):
    carreras = obtenerCarrerasDeDocente(request.user.id)
    
    #Obtengo las materias de la primera carrera
    materias = Materia.objects.filter(docente_id=request.user.id,actual=True,carrera_id=carreras[0][0])
    
    return render(request,"verAlumnosDocente.html",{"materias":materias,"carreras":carreras})

@login_required
@user_passes_test(lambda u: u.grupo == "Docente", login_url='autenticacion:iniciar_sesion') 
def obtenerAlumnosDeMateria(request,id):
    try:
        #Funcion que me da mis alumnos serializados de la materia
        alumnos = obtenerAlumnosDeMateriaDocente(idMateria=id,idDocente=request.user.id)
        
        return JsonResponse(alumnos,safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@user_passes_test(lambda u: u.grupo == "Docente", login_url='autenticacion:iniciar_sesion') 
def obtenerMateriasDeCarrera(request,id):
    try:
        #Me da mis materias serializadas, con id y nombre
        materias = obtenerMateriasDeCarreraDocente(idCarrera=id,idDocente=request.user.id)
        
        return JsonResponse(materias,safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@user_passes_test(lambda u: u.grupo == "Docente", login_url='autenticacion:iniciar_sesion') 
def notas(request,idMateria,idAlumno):
    if request.method == "GET":
        #Valido que el estudiante este en esta materia y que yo sea su docente y que este cursando y sea actual
        alumno_materia = get_object_or_404(
            Alumno_Materia,
            estudiante_id=idAlumno,
            materia_id=idMateria,
            materia__docente_id = request.user.id,
            materia__actual=True,
            estado="Cursando"
            )
        titulo = f"Notas de {alumno_materia.estudiante.first_name} {alumno_materia.estudiante.last_name} de la materia {alumno_materia.materia.nombre} de la carrera {alumno_materia.materia.carrera.nombre}"
        return render(request,"notas.html",{"titulo":titulo,"tipos":obtenerTiposNotas(),"idAlumno":idAlumno,"idMateria":idMateria})
    else:
        alumno = CustomUser.objects.get(id=idAlumno)
        materia = Materia.objects.get(id=idMateria)
        titulo = f"Notas de {alumno.first_name} {alumno.last_name} de la materia {materia.nombre} de la carrera {materia.carrera.nombre}"
        nota = ""
        try:
            try:   
                dia = datetime.datetime.strptime(request.POST["fecha"], '%Y-%m-%d')
            except:
                dia = None
            
            if request.POST["id"] == "":
                
                nota = Nota(nota=request.POST["nota"],tipo=request.POST["tipo"],dia=dia,observacion=request.POST["observacion"],alumno_id=idAlumno,materia_id=idMateria)
            else:
                validarQueIdDeNotaEsDeMiDocente(request.POST["id"],request.user.id)
                nota = Nota.objects.get(id=request.POST["id"],alumno_id=idAlumno,materia_id=idMateria)
                nota.dia = dia
                nota.nota =request.POST["nota"]
                nota.observacion = request.POST["observacion"]
                nota.tipo = request.POST["tipo"]
                print(nota.id)
                       
            errores = validarNota(nota)
            if len(errores) > 0:
                datos = {
                    "id":request.POST["id"],
                    "nota":nota.nota,
                    "tipo":nota.tipo,
                    "fecha":pasarFechaAString(dia),
                    "observacion":nota.observacion,

                }
                return render(request,"notas.html",{"titulo":titulo,"tipos":obtenerTiposNotas(),"errores":errores,"datos":datos,"idAlumno":idAlumno,"idMateria":idMateria})
            else:
                nota.save()
                return render(request,"notas.html",{"titulo":titulo,"tipos":obtenerTiposNotas(),"idAlumno":idAlumno,"idMateria":idMateria})              
        except Exception as e:
            print(e)
            return redirect("docente:ver_alumnos")
        
@login_required
@user_passes_test(lambda u: u.grupo == "Docente", login_url='autenticacion:iniciar_sesion') 
def obtenerNotas(request, idAlumno,idMateria):
    notas = Nota.objects.filter(alumno_id = idAlumno, materia_id = idMateria)
    notasSerializadas = []
    for nota in notas:
        notaSerializada ={
            "id":nota.id,
            "nota":nota.nota,
            "fecha":nota.dia,
            "tipo":nota.tipo,
            "observacion": modificarObservacion(nota.observacion)
        }
        
        notasSerializadas.append(notaSerializada)
    
    return JsonResponse(notasSerializadas,safe=False)

@login_required
@user_passes_test(lambda u: u.grupo == "Docente", login_url='autenticacion:iniciar_sesion') 
def obtenerNota(request,id):
    try:
        validarQueIdDeNotaEsDeMiDocente(id,request.user.id)
        nota = get_object_or_404(Nota,id=id)
        notaSerializada = {
            "id":nota.id,
            "nota":nota.nota,
            "fecha":nota.dia,
            "tipo":nota.tipo,
            "observacion": nota.observacion
        }
        return JsonResponse(notaSerializada,safe=False)
    except Exception as e: 
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@user_passes_test(lambda u: u.grupo == "Docente", login_url='autenticacion:iniciar_sesion') 
def eliminarNota(request):
    if request.method == "POST":
        try:
            validarQueIdDeNotaEsDeMiDocente(request.POST["id"],request.user.id)
            nota = Nota.objects.get(id=request.POST["id"])
            alumno = nota.alumno_id
            materia = nota.materia_id
            nota.delete()
            return redirect("docente:notas",materia,alumno)
        except Exception as e:
            print(e)

@login_required
@user_passes_test(lambda u: u.grupo == "Docente", login_url='autenticacion:iniciar_sesion') 
def aprobar(request,idAlumno,idMateria):
    try:
        #Obtengo si el estudiante esta en la materia, esta cursando es actual y soy su docente
        alumno_materia = get_object_or_404(
            Alumno_Materia,
            estudiante_id=idAlumno,
            materia_id=idMateria,
            materia__docente_id = request.user.id,
            materia__actual=True,
            estado="Cursando"
        )
            
        alumno_materia.estado = "Aprobado"
            
        alumno_materia.save()
        return redirect("docente:ver_alumnos")
    except Exception as e:
        print(e)
        return redirect("docente:notas",idMateria,idAlumno)
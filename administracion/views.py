from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearCarreraForm,CrearUsuarioForm,CrearMateriaForm
from django.http import JsonResponse
from .models import Carrera,CustomUser,Alumno_Carrera,Materia,Alumno_Materia,Correlativa
from .validar import validarCarrera,validarDocente,validarAlumno,validarMateria
from django.db import IntegrityError
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Case, When, Value, CharField, Subquery, Q
from django.views.decorators.csrf import csrf_protect
import json

# from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
#Views de las carreras
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def crearCarrera(request):
    if request.method == "GET":
        return render(request,"crearCarrera.html",{
            "form":CrearCarreraForm
            })
    else:
        form = CrearCarreraForm(request.POST)  
        try:     
            carrera = form.save(commit=False)        
            errores = validarCarrera(carrera)

            if len(errores) == 0:
                
                if request.POST["id"] == "":
                    carrera.save()
                else:
                    antiguaCarrera = get_object_or_404(Carrera,id = request.POST["id"])
                    carreraNueva = CrearCarreraForm(request.POST, instance=antiguaCarrera)
                    carreraNueva.save()
                
                return redirect("administracion:crearCarrera")
            else:
                return render(request,"crearCarrera.html",{
                "id":request.POST["id"],
                "form":form,
                "errores": errores
                })
        except ValueError:
            errores = ["Complete todos los campos"]
            return render(request,"crearCarrera.html",{
                "id":request.POST["id"],
                "form":form,
                "errores": errores
                })

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def eliminarCarrera(request):
    if request.method == "POST":
        carrera = get_object_or_404(Carrera,id = request.POST["id"])
        try:
            carrera.delete()
            return redirect("administracion:crearCarrera")
        except Exception as e:
            alumnos_carrera = Alumno_Carrera.objects.filter(carrera_id=carrera.id,estado="Cursando")
            
            if len(alumnos_carrera) != 0:
                return redirect("error/" + f"No se puede eliminar la carrera {carrera.nombre} porque hay alumnos inscriptos")
            
            materias = Materia.objects.filter(carrera_id=carrera.id)
            materias.update(actual=False)
            
            for materia in materias:     
                # Filtrar los registros que tengan el id en materia_id o correlativa_id
                registros_a_eliminar = Correlativa.objects.filter(Q(materia_id=materia.id) | Q(correlativa_id=materia.id))

                # Eliminar los registros
                registros_a_eliminar.delete()
            
            carrera.actual=False
            carrera.save()
            
            return redirect("administracion:crearCarrera")
            
            
        
    
#Funcion echa unicamente para obtener las carreras en el JavaScript
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def obtenerCarreras(request):
    carreras = Carrera.objects.filter(actual=True)
    carreras_serializadas = []

    for carrera in carreras:
        carrera_serializada = {
            "id": carrera.id,
            'nombre': carrera.nombre,
            'duracion': carrera.duracion,
            # Agrega más campos aquí si es necesario
        }
        carreras_serializadas.append(carrera_serializada)

    return JsonResponse(carreras_serializadas, safe=False)

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def obtenerIdCarrerasSegunAlumno(request,id):
    id_carreras = list(Alumno_Carrera.objects.filter(estudiante_id=id).values_list('carrera_id', flat=True))
    return JsonResponse(id_carreras, safe=False)

#Views de los docentes
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def crearDocente(request):
    if request.method == "GET":
        return render(request,"crearDocente.html",{
            "form":CrearUsuarioForm
            })
    else:
        form = CrearUsuarioForm(request.POST)
        #Por si ingresan el mismo usuario
        try:
            docente = ""
            #Ya que el form.save(commit=False) valida campos unicos como el username, debo fijarme si esto es un create o update, porque si o hiciera como a carreras, cunado quiera modificar a un usuraio, sin modificar el username, el from.save(commit=False) va a pensar que estoy creando otro usario con == usernmae, lo que me da un error, por eso debo primero ver si estoy haciendo un create o un update antes de hacer el resto
            if request.POST["id"]=="":
                docente = form.save(commit=False)
                docente.set_password(docente.username)
            else:
                antiguoDocente = get_object_or_404(CustomUser,id = request.POST["id"])
                nuevoDocente = CrearUsuarioForm(request.POST, instance=antiguoDocente)
                #Aca hago esto porque nuevo docente, tecnicamente sigue sienod un form, cunado uno hacer form.save... esta guardando un form, pero que sabe que esos datos son de un modelo, pero sigue siendo un form, por eso no puedo mandarlo a validar directo, primero debo hacer el save, para que me de un objeto de usuario y luego lo puedo validar, y ahora no me daria un error, porque ya hice el instance=antiguoDocente, por lo que ya sabe que es un update y no va a dar errores por tener == username
                docente = nuevoDocente.save(commit=False)

            docente.grupo = "Docente"
            errores = validarDocente(docente)
            if len(errores) == 0:
                
                docente.save()
                
                return redirect("administracion:crearDocente")
            
            else:
                return render(request,"crearDocente.html",{
                "id": request.POST["id"],
                "form":form,
                "errores": errores
                })
                
        except IntegrityError:
            docente = CustomUser(first_name=request.POST["first_name"],last_name=request.POST["last_name"],username=request.POST["username"],email=request.POST["email"])
            errores = validarDocente(docente)
            return render(request,"crearDocente.html",{
                "id": request.POST["id"],
                "form":form,
                "errores": errores
                })
            
        except ValueError as e:
            docente = CustomUser(first_name=request.POST["first_name"],last_name=request.POST["last_name"],username=request.POST["username"],email=request.POST["email"])
            errores = validarDocente(docente)
            return render(request,"crearDocente.html",{
                "id": request.POST["id"],
                "form":form,
                "errores": errores
                })
            
            
        
        
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def eliminarDocente(request):
    if request.method == "POST":
        print(request.POST["id"])
        docente = get_object_or_404(CustomUser,id = request.POST["id"])
        docente.delete()
        return redirect("administracion:crearDocente")

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def obtenerDocentes(request):
    docentes = CustomUser.objects.filter(grupo="Docente")
    docentes_serializados = []

    for docente in docentes:
        docente_serializado = {
            "id": docente.id,
            'nombre': docente.first_name,
            'apellido': docente.last_name,
            #El username es el dni
            'dni': docente.username,
            'email': docente.email,
            # Agrega más campos aquí si es necesario
        }
        docentes_serializados.append(docente_serializado)

    return JsonResponse(docentes_serializados, safe=False)

        
#Views de los alumnos
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def crearAlumno(request):
    if request.method == "GET":
        return render(request,"crearAlumno.html",{
            "form":CrearUsuarioForm,
            "carreras": Carrera.objects.all(),
            })
    else:
        form = CrearUsuarioForm(request.POST)
        #Por si ingresan el mismo usuario
        try:
            alumno = ""
            id_de_carreras_seleccionadas = request.POST.getlist("carreras")
            
            #Ya que el form.save(commit=False) valida campos unicos como el username, debo fijarme si esto es un create o update, porque si o hiciera como a carreras, cunado quiera modificar a un usuraio, sin modificar el username, el from.save(commit=False) va a pensar que estoy creando otro usario con == usernmae, lo que me da un error, por eso debo primero ver si estoy haciendo un create o un update antes de hacer el resto
            if request.POST["id"]=="":
                alumno = form.save(commit=False)
                alumno.set_password(alumno.username)
            else:
                antiguoAlumno = get_object_or_404(CustomUser,id = request.POST["id"])
                nuevoAlumno = CrearUsuarioForm(request.POST, instance=antiguoAlumno)
                #Aca hago esto porque nuevo docente, tecnicamente sigue sienod un form, cunado uno hacer form.save... esta guardando un form, pero que sabe que esos datos son de un modelo, pero sigue siendo un form, por eso no puedo mandarlo a validar directo, primero debo hacer el save, para que me de un objeto de usuario y luego lo puedo validar, y ahora no me daria un error, porque ya hice el instance=antiguoDocente, por lo que ya sabe que es un update y no va a dar errores por tener == username
                alumno = nuevoAlumno.save(commit=False)

            alumno.grupo = "Alumno"
            errores = validarAlumno(alumno,id_de_carreras_seleccionadas,list(Carrera.objects.values_list('id', flat=True)))
            if len(errores) == 0:
                with transaction.atomic():
                # Crear y guardar el usuario personalizado        
                    alumno.save()
                    
                    Alumno_Carrera.objects.filter(estudiante=alumno.id).delete()
                
                for id in id_de_carreras_seleccionadas:
                    carrera = Carrera.objects.get(pk=id)
                    Alumno_Carrera.objects.create(estudiante=alumno, carrera=carrera)
                
                return redirect("administracion:crearAlumno")
            
            else:
                id_carreras_en_numero = []
                
                for id in id_de_carreras_seleccionadas:
                    try:

                        if type(id) == str:
                            id_carreras_en_numero.append(int(id))
                        
                    except:
                        #Paso al seiguiente bucle
                        pass
                return render(request,"crearAlumno.html",{
                "id": request.POST["id"],
                "carreras": Carrera.objects.all(),
                "form":form,
                "id_seleccionados":id_carreras_en_numero,
                "errores": errores
                })
                
        except IntegrityError:
            alumno = CustomUser(first_name=request.POST["first_name"],last_name=request.POST["last_name"],username=request.POST["username"],email=request.POST["email"])
            errores = validarAlumno(alumno,id_de_carreras_seleccionadas,list(Carrera.objects.values_list('id', flat=True)))
            
            id_carreras_en_numero = []
                
            for id in id_de_carreras_seleccionadas:
                try:

                    if type(id) == str:
                       id_carreras_en_numero.append(int(id))
                        
                except:
                    #Paso al seiguiente bucle
                     pass
            
            return render(request,"crearAlumno.html",{
                "id": request.POST["id"],
                "carreras": Carrera.objects.all(),
                "form":form,
                "id_seleccionados":id_carreras_en_numero,
                "errores": errores
                })
            
        except ValueError as e:
            alumno = CustomUser(first_name=request.POST["first_name"],last_name=request.POST["last_name"],username=request.POST["username"],email=request.POST["email"])
            errores = validarAlumno(alumno,id_de_carreras_seleccionadas,list(Carrera.objects.values_list('id', flat=True)))
            
            id_carreras_en_numero = []
                
            for id in id_de_carreras_seleccionadas:
                try:

                    if type(id) == str:
                       id_carreras_en_numero.append(int(id))
                        
                except:
                    #Paso al seiguiente bucle
                     pass
            
            return render(request,"crearAlumno.html",{
                "id": request.POST["id"],
                "carreras": Carrera.objects.all(),
                "form":form,
                "id_seleccionados":id_carreras_en_numero,
                "errores": errores
                })     

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def eliminarAlumno(request):
    if request.method == "POST":
        alumno = get_object_or_404(CustomUser,id = request.POST["id"])
        alumno.delete()
        return redirect("administracion:crearAlumno")

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def obtenerAlumnos(request):
    alumnos = CustomUser.objects.filter(grupo="Alumno")
    alumnos_serializados = []

    for alumno in alumnos:
        alumno_serializados = {
            "id": alumno.id,
            'nombre': alumno.first_name,
            'apellido': alumno.last_name,
            #El username es el dni
            'dni': alumno.username,
            'email': alumno.email,
            # Agrega más campos aquí si es necesario
        }
        alumnos_serializados.append(alumno_serializados)

    return JsonResponse(alumnos_serializados, safe=False)


#Views de materias
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def crearMateria(request):
    if request.method == "GET":
        return render(request,"crearMateria.html",{
            "form":CrearMateriaForm
            })
    else:
        form = CrearMateriaForm(request.POST)
        
        if form.is_valid():
            try:
                materia = form.save(commit=False)    
                errores = validarMateria(materia)
                
                if len(errores) == 0:
                    
                    if request.POST["id"] == "":
                        materia.save()
                    else:
                        antiguaMateria = get_object_or_404(Materia,id = request.POST["id"])
                        materiaNueva = CrearMateriaForm(request.POST, instance=antiguaMateria)
                        materiaNueva.save()
                    
                    return redirect("administracion:crearMateria")
                else:
                    return render(request,"crearMateria.html",{
                    "id":request.POST["id"],
                    "form":form,
                    "errores": errores
                    })
                    
            except ValueError:
                errores = ["Complete todos los campos"]
                return render(request,"crearMateria.html",{
                    "id":request.POST["id"],
                    "form":form,
                    "errores": errores
                    })
        else:
            errores = []
            for error in form.errors:
                errores.append(f"Complete el campo {error}")
            return render(request, "crearMateria.html", {"form": form,"errores":errores})
            
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def eliminarMateria(request):
    if request.method == "POST":
        materia = get_object_or_404(Materia,id = request.POST["id"])
        try:
            materia.delete()
            return redirect("administracion:crearMateria")
        except Exception as e:
            alumno_materia = Alumno_Materia.objects.filter(materia_id=materia.id, estado="Cursando")
            if len(alumno_materia) != 0:
                return redirect("error/" + f"No se puede eliminar la materia {materia.nombre} de la carrera {materia.carrera.nombre} porque hay alumnos inscriptos")
            
            materia.actual = False
            # Filtrar los registros que tengan el id en materia_id o correlativa_id
            registros_a_eliminar = Correlativa.objects.filter(Q(materia_id=materia.id) | Q(correlativa_id=materia.id))

            # Eliminar los registros
            registros_a_eliminar.delete()
            
            materia.save()
            return redirect("administracion:crearMateria")

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
@csrf_protect
def guardarCorrelativas(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            materia = get_object_or_404(Materia,id=int(data["id"]))
            
            Correlativa.objects.filter(materia_id = materia.id).delete()
            
            materiasDeLaCarrera = Materia.objects.filter(carrera_id=materia.carrera.id)
            
            for dato in data["ids"]:
                if type(dato) == int:
                    #Con esto me valido que las correlativas sean de la misma carrera
                    if dato in materiasDeLaCarrera:
                        correlativa = Correlativa(materia_id = id,correlativa_id=dato)
                        correlativa.save()
                
                
            response_data = {'mensaje': 'Guardado exitoso'}
            return JsonResponse(response_data,status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Datos invalidos'}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
        
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def correlativas(request):
    if request.method == "POST":
        materia = get_object_or_404(Materia,id = request.POST["id"])
        return render(request,"correlativas.html",{
            "titulo": f"Correlativas de la materia {materia.nombre} de la carrera {materia.carrera.nombre}",
            "id":materia.id
        })
        
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def obtenerCorrelativas(request,id):
    
    materia = get_object_or_404(Materia,id=id)
    #hago una subconsulta donde obtego todas las correlativas de mi materia y me quedo solo con el campo correlativas_id, osea que subquery me dejaria con una lista de los id de las materias de las que soy correlativa
    subquery = Correlativa.objects.filter(materia_id=materia.id).values('correlativa_id')

        #Obtengo todas las materias de una carrera
    materias = Materia.objects.filter(
        carrera_id=materia.carrera.id
            #exclude saca la materia con el id de materia para sacar a la materia que uso como base
            #annotate esta creando una tercera columna llamada es_correlativa que se llenara dependiendo de un case, con su when
    ).exclude(id=materia.id).annotate(
        es_correlativa=Case(
                # id__in se refiere al campo id de la materia actual, y el operador __in verifica si ese id está en la lista de IDs de correlativas obtenida a través de la subconsulta.
            When(id__in=Subquery(subquery), then=Value('C')),
            default=Value(' '),
                #Este dato es el tipo de dato que debe ser un case, ya que las 2 opciones son C o "", es un tipo cahrField
            output_field=CharField()
        )
    ).values('id', 'nombre', 'es_correlativa').order_by('-es_correlativa', 'id')

    result_list = list(materias)

    return JsonResponse(result_list, safe=False)
        
        
            
            
        
    
#Funcion echa unicamente para obtener las carreras en el JavaScript
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def obtenerMaterias(request):
    
    materias = Materia.objects.filter(actual=True)
    materias_serializadas = []

    for materia in materias:
        materia_serializada = {
            "id": materia.id,
            'nombre': materia.nombre,
            'dia': materia.dia,
            "desde":materia.desde,
            "hasta":materia.hasta,
            "carrera":materia.carrera.nombre,
            "docente":f"{materia.docente.first_name} {materia.docente.last_name}"
            # Agrega más campos aquí si es necesario
        }
        materias_serializadas.append(materia_serializada)
        
    return JsonResponse(materias_serializadas, safe=False)

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def obtenerIdCarreraDocenteSegunMateria(request,id):
    materia = get_object_or_404(Materia,id=id)
    ids = [materia.carrera_id, materia.docente_id]
    
    return JsonResponse(ids, safe=False)

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def error(request,error):
    return render(request,"error.html",{"error":error})

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def alumnosCursando(request,dato):
    if request.method == "POST":
            
        titulo = ""
        
        if dato=="Carrera":
            carrera = Carrera.objects.get(pk=request.POST["id"])
            titulo = f"Alumnos de la carrera {carrera.nombre}"
            return render(request,"verAlumnos.html",{"titulo":titulo,"carrera":True,"id":request.POST["id"]})
        else:
            materia = Materia.objects.get(pk=request.POST["id"])
            titulo = f"Alumnos de la materia {materia.nombre} de la carrera {materia.carrera.nombre}"
            return render(request,"verAlumnos.html",{"titulo":titulo,"carrera":False,"id":request.POST["id"]})
        
@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def obtenerAlumnosSegunCarrera(request,id):
    alumnos_carrera = Alumno_Carrera.objects.filter(carrera_id=id)
    alumnos = []
    
    for alumno_carrera in alumnos_carrera:
        alumno_serializados = {
            "id": alumno_carrera.estudiante.id,
            'nombre': alumno_carrera.estudiante.first_name,
            'apellido': alumno_carrera.estudiante.last_name,
            #El username es el dni
            'dni': alumno_carrera.estudiante.username,
            'email': alumno_carrera.estudiante.email,

        }
        alumnos.append(alumno_serializados)

    return JsonResponse(alumnos, safe=False)

@login_required
@user_passes_test(lambda u: u.grupo == "Admin", login_url='autenticacion:iniciar_sesion') 
def obtenerAlumnosSegunMateria(request,id):
    alumnos_materia = Alumno_Materia.objects.filter(materia_id=id,estado="Cursando")
    alumnos = []
    
    for alumno_materia in alumnos_materia:
        alumno_serializados = {
            "id": alumno_materia.estudiante.id,
            'nombre': alumno_materia.estudiante.first_name,
            'apellido': alumno_materia.estudiante.last_name,
            #El username es el dni
            'dni': alumno_materia.estudiante.username,
            'email': alumno_materia.estudiante.email,

        }
        alumnos.append(alumno_serializados)

    
    return JsonResponse(alumnos, safe=False)


            
 





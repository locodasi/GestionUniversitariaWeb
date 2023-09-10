from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from administracion.models import CustomUser
from .validar import *

# Create your views here.
def iniciar_sesion(request):  
    if request.method == "GET":     
        # c = CustomUser(username="admin", grupo="admin")
        # c.set_password("admin")
        # c.save() 
        return render(request,"inicio_sesion.html",{
            "form": AuthenticationForm
        })
    else:
       u = authenticate(request, username=request.POST["username"], password = request.POST["password"])
       if u is None:
           return render(request,"inicio_sesion.html",{
            "form": AuthenticationForm,
            "error": "Usario o contraseña incorrecta"
            })
       else:
            login(request,u)
            dicc = obtenerDictConGrupos()
            return redirect(dicc.get(request.user.grupo).get("url")) 

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect("autenticacion:iniciar_sesion")

@login_required
def cambiar_contraseña(request):
    dicc = obtenerDictConGrupos()
    if request.method == "GET":       
        return render(request,"cambiarContra.html",{"nav":dicc.get(request.user.grupo).get("nav")}) 
    else:
        user = CustomUser.objects.get(id=request.user.id)
        
        if user.check_password(request.POST["vieja_contra"]):
            errores = validarContras(request.POST["nueva_contra"],request.POST["nueva_contra2"],request.user)

            if len(errores)==0:
                request.user.set_password(request.POST["nueva_contra"])
                request.user.save()
                #Este login es para vovler a iniciar la sesion despues del cambio de contraseña, si no lo hago y cambio la contra 2 veces seguidas, me saca la sesion y me reenvia al login
                login(request,request.user)               
                return redirect(dicc.get(request.user.grupo).get("url")) 
            else:
                return render(request,"cambiarContra.html",{"erroresContra":errores})  
            
        else:
            return render(request,"cambiarContra.html",{"erroresUsuario":["La antigua contraseña es incorrecta"]})  

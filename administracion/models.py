from django.db import models
from django.contrib.auth.models import AbstractUser

def nombre_materia(materia=None):
    return materia.nombre if materia else None

def usuario_alumno(user=None):
    return user.username if user else None

class CustomUser(AbstractUser):
    # Agrega aquí los campos adicionales para cada tipo de usuario
    grupo = models.CharField(max_length=100)
    carreras = models.ManyToManyField('Carrera', through='Alumno_Carrera')
    materias = models.ManyToManyField('Materia', through='Alumno_Materia')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    duracion = models.FloatField()
    actual = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    dia = models.CharField(max_length=12)
    desde = models.TimeField()
    hasta = models.TimeField()
    docente = models.ForeignKey(CustomUser,null=True, blank=True,on_delete=models.SET_NULL)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    actual = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.nombre}"

class Alumno_Carrera(models.Model):
    estudiante = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT)
    estado = models.CharField(max_length=50,default="Cursando")

class Alumno_Materia(models.Model):
    estudiante = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT)
    estado = models.CharField(max_length=50,default="Cursando")


class Nota(models.Model):
    alumno = models.ForeignKey(CustomUser,null=True, blank=True, on_delete=models.SET(usuario_alumno))
    materia = models.ForeignKey(Materia, null=True, blank=True, on_delete=models.SET(nombre_materia))
    nota = models.FloatField()
    tipo = models.CharField(max_length=20)
    dia = models.DateField()
    observacion = models.TextField(null=True,blank=True)

class Correlativa(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='Materia_materia')
    correlativa = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='Materia_correlativa')
    
    def __str__(self) -> str:
        return f"{self.correlativa.nombre} correlativa de {self.materia.nombre} "
    


from django import forms
from .models import Materia, Carrera, CustomUser
    
class CrearCarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields =["nombre","duracion"]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Matematicas II', 'class': 'form-control',"id":"nombre", 'autofocus': 'autofocus','tabindex': '1'}),
            'duracion': forms.TextInput(attrs={'type': 'number','max':'12','min':'0', 'step': '0.25', 'placeholder': '3.5', 'class': 'form-control',"id":"duracion",'tabindex': '2'}),
        }

class CrearUsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email"]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'DNI',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control', 'id': 'nombre', 'autofocus': 'autofocus', 'tabindex': '1'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control', 'id': 'apellido', 'tabindex': '2'}),
            'username': forms.TextInput(attrs={'type': 'number','max':'99999999','min':'11111111', 'step': '1', 'placeholder': '12345678', 'class': 'form-control',"id":"dni",'tabindex': '3'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control', 'id': 'email', 'tabindex': '4'}),
            # Agrega widgets y atributos adicionales para los campos 'carreras' y 'materias' si es necesario
        }

class CrearMateriaForm(forms.ModelForm):
    DIAS_SEMANA = (
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    )
    
    docente = forms.ModelChoiceField(queryset=CustomUser.objects.filter(grupo='Docente'),
                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'docente', 'tabindex': '3'}),
                                     to_field_name="id", empty_label=None)

    carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'carrera', 'tabindex': '4'}),
                                     to_field_name="id", empty_label=None)
    
    dia = forms.ChoiceField(choices=DIAS_SEMANA,
                            widget=forms.Select(attrs={'class': 'form-control', 'id': 'dia', 'tabindex': '2'}))

    class Meta:
        model = Materia
        fields = ["carrera", "nombre", "dia", "desde", "hasta", "docente"]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la materia', 'class': 'form-control', 'id': 'nombre', 'autofocus': 'autofocus', 'tabindex': '1'}),
            'desde': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'id': 'desde', 'tabindex': '5'}),
            'hasta': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'id': 'hasta', 'tabindex': '6'}),
        }




def validarContras(contra1,contra2,user):
    errores = []
    if contra1 != contra2:
        errores.append("Las contraseñas de confirmación no coinciden. Por favor, ingresa la misma nueva contraseña en ambos campos.")
        
        return errores
        
    if contra1.isnumeric():
        errores.append("La nueva contraseña no puede ser unicamente numerica")
    
    if len(contra1) < 8:
        errores.append("La nueva contraseña no puede tener menos de 8 caracteres")
        
    contrasComunes=["qwerty123","qwertyui","contraseña","password","1q2w3e4r5t"]
    
    if contra1 in contrasComunes:
        errores.append("La nueva contraseña es muy comun")
        
    if user.first_name.find(contra1) != -1 or user.last_name.find(contra1) != -1 or user.username.find(contra1) != -1 or user.email.find(contra1) != -1:
        errores.append("La nueva contraseña es muy similar a otra informacion personal")
    
    return errores

def obtenerDictConGrupos():
    diccionario={
        "Admin": {"url":"administracion:crearCarrera","nav":"nav.html"},
        "Alumno":{"url":"alumno:seleccion_materias","nav":"navAlumno.html"},
        "Docente":{"url":"docente:ver_alumnos","nav":"navDocente.html"},
    }
    
    return diccionario
    
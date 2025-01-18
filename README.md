# Página Universitaria  

**Sistema de Gestión Universitaria** desarrollado en **Django**, con funcionalidades dinámicas implementadas en **JavaScript**, y soporte para base de datos en **MySQL** gestionada con **Workbench**.  

El proyecto está desplegado en [Render](https://render.com), lo que facilita su acceso y uso por parte de alumnos, docentes y administradores.  

## Funcionalidades  

### Roles y Permisos  
- **Alumno:**  
  - Registro en materias habilitadas según correlativas.  
  - Consulta de notas y observaciones de los docentes.  

- **Docente:**  
  - Registro y modificación de calificaciones de alumnos en sus materias asignadas.  

- **Administrador:**  
  - Gestión integral de usuarios (alumnos y docentes), materias y carreras.  

---

## Detalle de Aplicaciones  

El sistema está organizado en diferentes **aplicaciones** dentro del proyecto Django, cada una dedicada a una funcionalidad específica:  

### **Autenticación**  
- Gestión de inicios de sesión para todos los usuarios (alumnos, docentes, administradores).  
- Funcionalidad para el cambio de contraseñas.  

### **Administración**  
- Herramientas para la administración del sitio:  
  - **Gestión de Alumnos, Docentes y Materias:** permite la creación, modificación y eliminación de registros.  
  - Control integral de la información académica y de usuarios.  

### **Alumno**  
- Funcionalidades para los estudiantes:  
  - Inscripción y baja de materias habilitadas según correlativas.  
  - Consulta de notas y observaciones registradas por los docentes.  

### **Docente**  
- Funcionalidades para los profesores:  
  - Registro de calificaciones para los alumnos de sus materias asignadas.  
  - Aprobación de alumnos con base en las notas registradas.  


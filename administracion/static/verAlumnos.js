const carrera = document.getElementById("carrera");
const id = document.getElementById("id");

const formatearAlumno = (alumno)=>{
    let alumnoFormateado = alumno.id.toString().padStart(5,"0") + " " + alumno.nombre.padEnd(50," ") + " " + alumno.apellido.padEnd(50," ") + " " + alumno.dni + " " + alumno.email.padEnd(70," ")
    return alumnoFormateado;
}

const obtenerAlumnos = async () => {
    try{
        let respuesta = "";
        if(carrera.innerHTML == "True"){
            respuesta = await fetch('/administracion/obtenerAlumnos/carrera/' + id.innerHTML);  // Cambia la URL según tu configuración
        }else{
            respuesta = await fetch('/administracion/obtenerAlumnos/materia/' + id.innerHTML);  // Cambia la URL según tu configuración
        }
        const data = await respuesta.json();
        const alumnos = data.map(alumno => formatearAlumno(alumno));
        return alumnos;

    } catch (error) {
        console.error('Error al obtener los alumnos:', error);
        return [];
    }
         
}

document.addEventListener("DOMContentLoaded", async () => {
    const busqueda = document.getElementById("busqueda");
    const opciones = document.getElementById("opciones");
    const pre = document.getElementById("pre");

    pre.textContent = "ID" + " ".repeat(4) + "Nombre" + " ".repeat(45) + "Apellido" + " ".repeat(43) + "DNI" + " ".repeat(6) + "Email"

    const op = await obtenerAlumnos();

        mostrarOpciones = ()=>{
            fragmento = document.createDocumentFragment();
            op.forEach(opcion =>{
                const opcionElemento = document.createElement("pre");
                opcionElemento.textContent = opcion;

                fragmento.appendChild(opcionElemento);
            });

            opciones.appendChild(fragmento);
        }
  
      mostrarOpciones();
  
    // Función para mostrar las opciones coincidentes en la lista
    mostrarOpcionesCoincidentes = (termino) => {
        opciones.innerHTML = ""; // Limpiar la lista antes de mostrar las opciones
        if(termino == ""){
            mostrarOpciones();
        }else{
            const opcionesCoincidentes = op.filter(opcion => opcion.toLowerCase().includes(termino.toLowerCase()));
            fragmento = document.createDocumentFragment();
            opcionesCoincidentes.forEach(opcion => {
                const opcionElemento = document.createElement("pre");
                opcionElemento.textContent = opcion;
                fragmento.appendChild(opcionElemento);

             });

             opciones.appendChild(fragmento);
          
        }
    }
  
    // Escuchar el evento de entrada en el campo de búsqueda
    busqueda.addEventListener("input",()=>{
      const terminoDeBusqueda = busqueda.value;
      mostrarOpcionesCoincidentes(terminoDeBusqueda);
    });
  
  });
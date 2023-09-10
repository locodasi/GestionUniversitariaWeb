document.addEventListener("DOMContentLoaded",  () => {
    const busqueda = document.getElementById("busqueda");
    const pre = document.getElementById("pre");
    const materia = document.getElementById("selectMateria");
    const carrera = document.getElementById("selectCarrera");

    pre.textContent = "ID" + " ".repeat(4) + "Nombre" + " ".repeat(45) + "Apellido" + " ".repeat(43) + "DNI" + " ".repeat(6) + "Email"

    obtenerAlumnos(materia.value);

    materia.addEventListener("change",()=>{
        obtenerAlumnos(materia.value);
    })

    carrera.addEventListener("change",()=>{
        //Primero obtengo las nuevas materias
        materias= obtenerMaterias(carrera.value);
    })
  
    // Escuchar el evento de entrada en el campo de búsqueda
    busqueda.addEventListener("input",()=>{
      const terminoDeBusqueda = busqueda.value;
      mostrarOpcionesCoincidentes(terminoDeBusqueda);
    });
  
});

obtenerAlumnos= async (idMateria)=>{
    const opciones = document.getElementById("opciones");

    opciones.innerHTML = "";//Limpio cada cambio

    const op = await obtenerAlumnosJson(idMateria);

    mostrarOpciones = ()=>{
        fragmento = document.createDocumentFragment();
        op.forEach(opcion =>{
            const opcionElemento = document.createElement("pre");
            opcionElemento.textContent = opcion;
            opcionElemento.setAttribute("style","font-size: 14px;")
            darleEventoAOption(opcionElemento);
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
                opcionElemento.setAttribute("style","font-size: 14px;")
                darleEventoAOption(opcionElemento);
                fragmento.appendChild(opcionElemento);

            });

            opciones.appendChild(fragmento);
        
        }
    }  
}

const obtenerAlumnosJson = async (idMateria) => {
    try{

        const respuesta = await fetch('/docente/obtenerAlumnosDeMateria/' + idMateria);  // Cambia la URL según tu configuración
        const data = await respuesta.json();
        const alumnos = data.map(alumno => formatearAlumno(alumno));
        return alumnos;

    } catch (error) {
        location.reload();
        // console.error('Error al obtener los alumnos:', error);
        // return [];
    }
         
}

const formatearAlumno = (alumno)=>{
    let alumnoFormateado = alumno.id.toString().padStart(5,"0") + " " + alumno.nombre.padEnd(50," ") + " " + alumno.apellido.padEnd(50," ") + " " + alumno.dni + " " + alumno.email.padEnd(70," ")
    return alumnoFormateado;
}

const obtenerMaterias = async (idCarrera) =>{
    const materias = await obtenerMateriasJson(idCarrera)
    agregarMaterias(materias,document.getElementById("selectMateria"));
}

const obtenerMateriasJson=async(idCarrera)=>{
    try{
        const respuesta = await fetch('/docente/obtenerMateriasDeCarrera/' + idCarrera);  // Cambia la URL según tu configuración
        const data = await respuesta.json();
        const materias = data.map(materia => ({id:materia.id,nombre:materia.nombre}));
        return materias;
    } catch (error) {
        location.reload();
        // console.error('Error al obtener los alumnos:', error);
        // return [];
    }
}

agregarMaterias = (materias,selectMateria)=>{
    selectMateria.innerHTML = "";
    const fragmento = document.createDocumentFragment();

    for(materia of materias){
        const option = document.createElement("OPTION");
        option.value = materia.id;
        option.innerHTML = materia.nombre;
        fragmento.appendChild(option);
    }

    selectMateria.appendChild(fragmento);

    obtenerAlumnos(selectMateria.value);
}

const darleEventoAOption = (option)=>{
    let url = "/docente/notas/" + document.getElementById("selectMateria").value + "/" + parseInt(option.innerHTML.slice(0,5));
    option.addEventListener("dblclick",()=>{
       window.location.href = url;
    });
}

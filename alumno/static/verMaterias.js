const formatearMateria = (materia)=>{
    let materiaFormateada = materia.idMateria.toString().padStart(5,"0") + " " + materia.nombreMateria.padEnd(50," ") + " " +  materia.correlativasMateria

    return materiaFormateada;
}



const obtenerMateriasJson = async (carreraId) => {
    try{

        const respuesta = await fetch('/alumno/obtenerMateriasConCorrelativas/' + carreraId);  // Cambia la URL según tu configuración
        const data = await respuesta.json();
        const materias = data.map(materia => formatearMateria(materia));
        return materias;

    } catch (error) {
        // location.reload();
        console.error('Error al obtener las carreras:', error);
        return [];
    }
         
}

document.addEventListener("DOMContentLoaded", async () => {
    const busqueda = document.getElementById("busqueda");
    const carrera = document.getElementById("carrera");

    const pre = document.getElementById("pre");

    pre.textContent = "ID" + " ".repeat(4) + "Materia" + " ".repeat(44) + "Correlativas"

    obtenerMaterias(carrera.value);

    // Escuchar el evento de entrada en el campo de búsqueda
    busqueda.addEventListener("input",()=>{
      const terminoDeBusqueda = busqueda.value;
      mostrarOpcionesCoincidentes(terminoDeBusqueda);
    });

    carrera.addEventListener("change",()=>{
        obtenerMaterias(carrera.value);
    })
});

obtenerMaterias = async (idCarrera)=>{
    const opciones = document.getElementById("opciones");

    opciones.innerHTML = "";//Limpio cada cambio

    const op = await obtenerMateriasJson(idCarrera);

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
}
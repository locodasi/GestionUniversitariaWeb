document.addEventListener("DOMContentLoaded", async ()=>{
    const busqueda = document.getElementById("busqueda");
    const carrera = document.getElementById("carrera");

    const pre = document.getElementById("pre");

    pre.setAttribute("style","font-size: 14px;")
    pre.textContent = "ID" + " ".repeat(4) + "Fecha" + " ".repeat(6) + "Nota" + " ".repeat(3) + "Tipo" + " ".repeat(14) + "Observacion"

    const op = await obtenerNotas();

    mostrarOpciones(op);

    // Escuchar el evento de entrada en el campo de búsqueda
    busqueda.addEventListener("input",()=>{
        const terminoDeBusqueda = busqueda.value;
        mostrarOpcionesCoincidentes(op,terminoDeBusqueda);
    });

});

mostrarOpciones = (op)=>{
    fragmento = document.createDocumentFragment();
    op.forEach(opcion =>{
        const opcionElemento = document.createElement("pre");
        opcionElemento.textContent = opcion;
        opcionElemento.setAttribute("style","font-size: 14px;")
        darleEvento(opcionElemento);
        fragmento.appendChild(opcionElemento);
    });

    opciones.appendChild(fragmento);
}

mostrarOpcionesCoincidentes = (op,termino) => {
    const opciones = document.getElementById("opciones");
    opciones.innerHTML = ""; // Limpiar la lista antes de mostrar las opciones
    if(termino == ""){
        mostrarOpciones(op);
    }else{
        const opcionesCoincidentes = op.filter(opcion => opcion.toLowerCase().includes(termino.toLowerCase()));
        fragmento = document.createDocumentFragment();
        opcionesCoincidentes.forEach(opcion => {
            const opcionElemento = document.createElement("pre");
            opcionElemento.textContent = opcion;
            opcionElemento.setAttribute("style","font-size: 14px;")
            darleEvento(opcionElemento);
            fragmento.appendChild(opcionElemento);

        });

        opciones.appendChild(fragmento);
    
    }
}

const obtenerNotas = async () => {
    try{
        const id = document.getElementById("id");
        const respuesta = await fetch('/alumno/obtenerNotas/' + id.innerHTML);  // Cambia la URL según tu configuración
        const data = await respuesta.json();
        const notas = data.map(nota => formatearNota(nota));
        return notas;

    } catch (error) {
        console.error('Error al obtener las notas:', error);
        return [];
    }
         
}

const formatearNota = (nota)=>{
    let notaFormateada = nota.id.toString().padStart(5,"0") + " " + parsearFecha(nota.fecha) + " " + nota.nota.toString().padStart(2,"0") + "     " + nota.tipo.padEnd(17," ") + " " + nota.observacion
    return notaFormateada;
}

parsearFecha = fecha =>{
    parteDeFecha = fecha.split("-");
    return parteDeFecha[2] + "/" + parteDeFecha[1] + "/" + parteDeFecha[0];
}

const darleEvento = (opcion)=>{
    opcion.addEventListener("dblclick", async ()=>{
        try{
            const respuesta = await fetch('/alumno/obtenerObservacion/' + parseInt(opcion.innerHTML.substring(0,6)));  // Cambia la URL según tu configuración
            const dato = await respuesta.json();
            const obs = document.getElementById("observacion");
            obs.value = dato;
        } catch (error) {
            location.reload();
            // return [];
        }
    })
}
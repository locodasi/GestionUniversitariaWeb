const pasarFocus = ()=>{
    const camposDeForm = document.querySelectorAll(".form-control");

    camposDeForm.forEach((campo, indice) => {

        if(! (indice >= (camposDeForm.length - 1))){
            campo.addEventListener("keydown", (event) => {
                if (event.key === "Enter") {
                    if( ! (indice == camposDeForm.length -2)){
                        event.preventDefault();
                        const proximoIndice = indice + 1;
                        if (proximoIndice < camposDeForm.length) {
                            camposDeForm[proximoIndice].focus();
                        }
                    }
                }
            });
        }
    });
};

const remplazar = (elemento,atributo)=>{
    if(atributo == "is-valid"){
        elemento.classList.add("is-valid");
        elemento.classList.remove("is-invalid");
    }else{
        elemento.classList.add("is-invalid");
        elemento.classList.remove("is-valid");
    }
};

// const ponerHoraActual = ()=>{
//     // Obtiene el campo de entrada de fecha por su ID
//     let fechaInput = document.getElementById("fecha");

//     // Obtiene la fecha actual
//     let fechaActual = new Date();

//     // Formatea la fecha actual en el formato "YYYY-MM-DD" (que es el formato de dateInput)
//     let fechaFormateada = fechaActual.getFullYear() + "-" + 
//                          String(fechaActual.getMonth() + 1).padStart(2, '0') + "-" + 
//                          String(fechaActual.getDate()).padStart(2, '0');

//     // Establece el valor predeterminado del campo de entrada de fecha
//     fechaInput.value = fechaFormateada;
// };

document.getElementById("limpiar").addEventListener("click",(e)=>{
    const camposDeForm = document.querySelectorAll(".form-control");

    for(campo of camposDeForm){
        //Para que no me borre el select
        if(campo.type !== "select-one"){
            campo.value = "";
        }        
    }

    const id = document.getElementById("id");
    id.value="";

    const eliminar = document.getElementById("eliminar");
    const aprobar = document.getElementById("aprobar");

    eliminar.setAttribute("hidden","");

    e.preventDefault();
    camposDeForm[0].focus();
});

document.getElementById("enviar").addEventListener("click",(e)=>{
    //Asi agararo os form-control dentro de form
    const camposDeForm = document.getElementById("form").querySelectorAll(".form-control");
    let flag = true;
    for(campo in camposDeForm){
        //asi no cuenta el observaciones
        if(campo < camposDeForm.length - 1){
            if(camposDeForm[campo].value == ""){
                remplazar(camposDeForm[campo],"is-invalid");
                flag = false;
            }else{
                camposDeForm[campo].classList.remove("is-valid");
                camposDeForm[campo].classList.remove("is-invalid");
            }  
        }else{
            //Para que corte el bucle y no siga
            break;
        }        
    }

    if(!flag && !validarFecha()){
        e.preventDefault();
    }
});

const nota = document.getElementById("nota");
nota.addEventListener("input",()=>{
    let valor = parseFloat(nota.value);
    if(valor > 10 || valor < 1){
        nota.value = 10;
    }

});


const validarFecha =()=>{
    const fecha = document.getElementById("fecha");
    // Obtiene la fecha actual
    let fechaActual = new Date();

    // Obtiene la fecha ingresada en el campo dateInput
    let fechaIngresada = new Date(fecha.value);

    // Compara las fechas
    if (fechaIngresada > fechaActual) {
        remplazar(fecha,"is-invalid");
        return false;
    }

    return true;
}

//Para darles estilos a los campos segun la validacion del backend
erroresDadosPorBackend = ()=>{
    const errores = document.querySelectorAll(".error");

    //primero veo si hay erroes, porque ya que esto siempre se hace cunado se carga la pagina, puedo ni validar nada y ya se me estarian poniendo los campos como validos
    if(errores.length > 0){
        elementos = {"nota":document.getElementById("nota"),"tipo":document.getElementById("tipo"),"fecha":document.getElementById("fecha")};
        //Si un error contiene el nombre de un campo entonces es invalido
        errores.forEach(error=>{
            if(error.textContent.toLowerCase().includes("nota")){
                nota.classList.add("is-invalid");
                nota.classList.remove("is-valid");
                delete elementos["nota"];
            }

            if(error.textContent.toLowerCase().includes("tipo")){
                tipo = document.getElementById("tipo");
                tipo.classList.add("is-invalid");
                tipo.classList.remove("is-valid");
                delete elementos["tipo"];
            }

            if(error.textContent.toLowerCase().includes("fecha")){
                tipo = document.getElementById("fecha");
                fecha.classList.add("is-invalid");
                fecha.classList.remove("is-valid");
                delete elementos["fecha"];
            }

        })

        for(let elemento of Object.values(elementos)){
            elemento.classList.add("is-valid");
            elemento.classList.remove("is-invalid");
        }
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

const obtenerNotas = async () => {
    try{
        const idAlumno = document.getElementById("idAlumno");
        const idMateria = document.getElementById("idMateria");
        const respuesta = await fetch('/docente/notas/obtenerNotas/' + idAlumno.innerHTML + "/" + idMateria.innerHTML);  // Cambia la URL según tu configuración
        const data = await respuesta.json();
        const notas = data.map(nota => formatearNota(nota));
        return notas;

    } catch (error) {
        console.error('Error al obtener las notas:', error);
        return [];
    }
         
}


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

document.addEventListener("DOMContentLoaded",  async () => {
    pasarFocus();
    erroresDadosPorBackend();

    const busqueda = document.getElementById("busqueda");
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

    validarAprobar();
   
});

validarAprobar=()=>{
    const aprobar = document.getElementById("aprobar");
    const opciones = document.getElementById("opciones");

    if(opciones.childElementCount > 0){
        aprobar.removeAttribute("hidden");
    }
}

const darleEvento = (opcion)=>{
    opcion.addEventListener("click", async ()=>{
        try{
            const respuesta = await fetch('/docente/notas/obtenerNotaJson/' + parseInt(opcion.innerHTML.substring(0,6)));  // Cambia la URL según tu configuración
            const nota = await respuesta.json();
            ponerLosDatos(nota);    
        } catch (error) {
            console.log(error);
            // return [];
        }
    })
}

ponerLosDatos = datosNota =>{
    nota.value = datosNota.nota;

    id = document.getElementById("id");
    tipo = document.getElementById("tipo");
    fecha = document.getElementById("fecha");
    observacion = document.getElementById("observacion");

    id.value = datosNota.id;
    observacion.value = datosNota.observacion;
    tipo.value = datosNota.tipo;
    fecha.value = datosNota.fecha;

    const eliminar = document.getElementById("eliminar");

    eliminar.removeAttribute("hidden");
}

document.getElementById("aprobar").addEventListener("click", (event) => {
    event.preventDefault(); // Evitar el envío predeterminado del formulario

    url = aprobar.getAttribute("formaction");
        // Redirigir a la URL especificada en el frontend
    window.location.href = url;
});



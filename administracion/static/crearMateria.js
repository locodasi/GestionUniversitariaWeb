const id = document.getElementById("id");

const carrera = document.getElementById("carrera");
const nombre = document.getElementById("nombre");
const dia = document.getElementById("dia");
const desde = document.getElementById("desde");
const hasta = document.getElementById("hasta");
const docente = document.getElementById("docente");

const limpiar = document.getElementById("limpiar");
const eliminar = document.getElementById("eliminar");
const enviar = document.getElementById("enviar");
const verAlumnos = document.getElementById("verAlumnos");
const correlativas = document.getElementById("correlativas");

const remplazar = (elemento,atributo)=>{
    if(atributo == "is-valid"){
        elemento.classList.add("is-valid");
        elemento.classList.remove("is-invalid");
    }else{
        elemento.classList.add("is-invalid");
        elemento.classList.remove("is-valid");
    }
};

nombre.addEventListener("input",()=>{
    if(nombre.value.length > 100 ){
        nombre.value = nombre.value.substring(0,100);
    }
});


limpiar.addEventListener("click",(e)=>{

    const form = document.getElementById("form");
    let flag = true;
    for(hijo of form.children){
        if(hijo.tagName === "INPUT" && hijo.type != "hidden"){
            hijo.value = "";
            hijo.classList.remove("is-valid");
            hijo.classList.remove("is-invalid");
        }
    }

    eliminar.setAttribute("hidden","");
    verAlumnos.setAttribute("hidden","");
    correlativas.setAttribute("hidden","");

    e.preventDefault()
});

enviar.addEventListener("click",(e)=>{
    const form = document.getElementById("form");
    let flag = true;
    for(hijo of form.children){
        if(hijo.tagName === "INPUT" && hijo.type != "hidden"){
            if(hijo.value == ""){
                remplazar(hijo,"is-invalid");
                flag = false;
            }else{
                hijo.classList.remove("is-valid");
                hijo.classList.remove("is-invalid");
            }
        }
    }

    if(!flag){
        e.preventDefault();
    }
});

pasarFocus = ()=>{
    const camposDeForm = document.querySelectorAll(".form-control");

    camposDeForm.forEach((campo, indice) => {

        if(! (indice >= (camposDeForm.length - 1))){
            campo.addEventListener("keydown", (event) => {
                if (event.key === "Enter") {
                    if(indice == camposDeForm.length -2){
                        console.log(camposDeForm)
                        enviar.click();
                    }else{
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
}

const formatearMateria = (materia)=>{
    let materiaFormateada = materia.id.toString().padStart(5,"0") + " " + materia.carrera.padEnd(50," ") + " " + materia.nombre.padEnd(50," ") + " " + materia.dia.padEnd(9," ") + " " + materia.desde.substring(0,5).padStart(5," ") + " " + materia.hasta.substring(0,5).padStart(5," ") + " " + materia.docente;

    return materiaFormateada;
}

const obtenerMaterias = async () => {
    try{

        const respuesta = await fetch('/administracion/obtenerMaterias/');  // Cambia la URL según tu configuración
        const data = await respuesta.json();
        const materias = data.map(materia => formatearMateria(materia));
        return materias;

    } catch (error) {
        console.error('Error al obtener las carreras:', error);
        return [];
    }
         
}

const obtenerIdCarreraDocenteSegunMateria = async id =>{
    try{

        const respuesta = await fetch('/administracion/obtenerIdCarreraDocenteSegunMateria/' + id);  // Cambia la URL según tu configuración
        const data = await respuesta.json();
        const ids = data.map(id => id);
        return ids;

    } catch (error) {
        console.error('Error al obtener los ids:', error);
        return [];
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    pasarFocus();

    const busqueda = document.getElementById("busqueda");
    const opciones = document.getElementById("opciones");
    const pre = document.getElementById("pre");

    pre.textContent = "ID" + " ".repeat(4) + "Carrera" + " ".repeat(45) + "Materia" + " ".repeat(43) + "Dia" + " ".repeat(7) + "Desde" + " Hasta " + "Docente" 

    const op = await obtenerMaterias();
    
    mostrarOpciones = ()=>{
        fragmento = document.createDocumentFragment();
        op.forEach(opcion =>{
            const opcionElemento = document.createElement("pre");
            opcionElemento.textContent = opcion;


            opcionElemento.addEventListener("click",async ()=> {
                id.value = parseInt(opcion.substring(0,5));
                nombre.value = opcion.substring(57, 107).trim();   
                desde.value = opcion.substring(118,123);
                hasta.value = opcion.substring(124, 129);

                for (const op of dia.options) {
                    if (op.value == opcion.substring(108,118).trim()) {
                        op.selected = true;
                    }
                }

                let ids = await obtenerIdCarreraDocenteSegunMateria(parseInt(opcion.substring(0,5)));
                
                for (const op of carrera.options) {
                    if (op.value == ids[0]) {
                        op.selected = true;
                    }
                }

                for (const op of docente.options) {
                    if (op.value == ids[1]) {
                        op.selected = true;
                    }
                }

                eliminar.removeAttribute("hidden");
                verAlumnos.removeAttribute("hidden");
                correlativas.removeAttribute("hidden");
            });

            fragmento.appendChild(opcionElemento);
        });

        opciones.appendChild(fragmento);
    }

    mostrarOpciones();

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

                opcionElemento.addEventListener("click",async()=> {
                    id.value = parseInt(opcion.substring(0,5));
                    nombre.value = opcion.substring(57, 107).trim();   
                    desde.value = opcion.substring(118,123);
                    hasta.value = opcion.substring(124, 129);

                    for (const op of dia.options) {
                        if (op.value == opcion.substring(108,118).trim()) {
                            op.selected = true;
                        }
                    }

                    let ids = await obtenerIdCarreraDocenteSegunMateria(parseInt(opcion.substring(0,5)));
                    
                    for (const op of carrera.options) {
                        if (op.value == ids[0]) {
                            op.selected = true;
                        }
                    }

                    for (const op of docente.options) {
                        if (op.value == ids[1]) {
                            op.selected = true;
                        }
                    }
                    
                    eliminar.removeAttribute("hidden");
                    verAlumnos.removeAttribute("hidden");
                    correlativas.removeAttribute("hidden");
                });

                fragmento.appendChild(opcionElemento);

            });

            opciones.appendChild(fragmento);
        
        }
    }

    erroresDadosPorBackend = ()=>{
        const errores = document.querySelectorAll(".error");

        //primero veo si hay erroes, porque ya que esto siempre se hace cunado se carga la pagina, puedo ni validar nada y ya se me estarian poniendo los campos como validos
        if(errores.length > 0){
            elementos = {"nombre":nombre,"carrera":carrera,"desde":desde,"hasta":hasta,"docente":docente,"dia":dia};
            //Si un error contiene el nombre de un campo entonces es invalido
            errores.forEach(error=>{
                if(error.textContent.includes("nombre")){
                    nombre.classList.add("is-invalid");
                    nombre.classList.remove("is-valid");
                    delete elementos["nombre"];
                }

                if(error.textContent.includes("carrera")){
                    carrera.classList.add("is-invalid");
                    carrera.classList.remove("is-valid");
                    delete elementos["carrera"];
                }

                if(error.textContent.includes("dia")){
                    dia.classList.add("is-invalid");
                    dia.classList.remove("is-valid");
                    delete elementos["dia"];
                }

                if(error.textContent.includes("docente")){
                    docente.classList.add("is-invalid");
                    docente.classList.remove("is-valid");
                    delete elementos["docente"];
                }

                if(error.textContent.includes("Desde")){
                    desde.classList.add("is-invalid");
                    desde.classList.remove("is-valid");
                    delete elementos["desde"];
                }

                if(error.textContent.includes("hasta") || error.textContent.includes("intervalo")){
                    hasta.classList.add("is-invalid");
                    hasta.classList.remove("is-valid");
                    delete elementos["hasta"];
                }

                if(error.textContent.includes("Complete todos los campos")){
                    console.log
                    for(let elemento in elementos){
                        if(elementos[elemento].value == ""){
                            elementos[elemento].classList.add("is-invalid");
                            elementos[elemento].classList.add("is-valid");
                        }
                        elementos[elemento].classList.remove("is-valid");
                        elementos[elemento].classList.remove("is-invalid");
                    }

                    elementos = {};
                }

            })

            for(let elemento of Object.values(elementos)){
                elemento.classList.add("is-valid");
                elemento.classList.remove("is-invalid");
            }
        }

    }

    erroresDadosPorBackend();

  
    // Escuchar el evento de entrada en el campo de búsqueda
    busqueda.addEventListener("input",()=>{
      const terminoDeBusqueda = busqueda.value;
      mostrarOpcionesCoincidentes(terminoDeBusqueda);
    });
  
});
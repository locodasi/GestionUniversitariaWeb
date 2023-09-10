const id = document.getElementById("id");

const nombre = document.getElementById("nombre");
const apellido = document.getElementById("apellido");
const dni = document.getElementById("dni")
const email = document.getElementById("email")

const limpiar = document.getElementById("limpiar");
const eliminar = document.getElementById("eliminar");
const enviar = document.getElementById("enviar");

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
    if(nombre.value.length > 50 ){
        nombre.value = nombre.value.substring(0,50);
    }
});

nombre.addEventListener("keydown",(event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        apellido.focus();
    }
});

apellido.addEventListener("input",()=>{
    if(apellido.value.length > 50 ){
        apellido.value = apellido.value.substring(0,50);
    }
});

apellido.addEventListener("keydown",(event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        dni.focus();
    }
});

dni.addEventListener("input",()=>{
    if(dni.value.length > 8 ){
        dni.value = dni.value.substring(0,8);
    }
});

dni.addEventListener("keydown",(event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        email.focus();
    }
});


limpiar.addEventListener("click",(e)=>{
    id.value = "";
    nombre.value = "";
    apellido.value = "";
    dni.value = ""
    email.value = ""
    eliminar.setAttribute("hidden","");

    nombre.classList.remove("is-valid");
    nombre.classList.remove("is-invalid");

    apellido.classList.remove("is-valid");
    apellido.classList.remove("is-invalid");

    dni.classList.remove("is-valid");
    dni.classList.remove("is-invalid");

    email.classList.remove("is-valid");
    email.classList.remove("is-invalid");
    
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





const formatearDocente = (docente)=>{
    let docenteFormateado = docente.id.toString().padStart(5,"0") + " " + docente.nombre.padEnd(50," ") + " " + docente.apellido.padEnd(50," ") + " " + docente.dni + " " + docente.email.padEnd(70," ")
    return docenteFormateado;
}

const obtenerDocentes = async () => {
    try{

        const respuesta = await fetch('/administracion/obtenerDocentes/');  // Cambia la URL según tu configuración
        const data = await respuesta.json();
        const docentes = data.map(docente => formatearDocente(docente));
        return docentes;

    } catch (error) {
        console.error('Error al obtener los docentes:', error);
        return [];
    }
         
}

document.addEventListener("DOMContentLoaded", async () => {
    const busqueda = document.getElementById("busqueda");
    const opciones = document.getElementById("opciones");
    const pre = document.getElementById("pre");

    pre.textContent = "ID" + " ".repeat(4) + "Nombre" + " ".repeat(45) + "Apellido" + " ".repeat(43) + "DNI" + " ".repeat(6) + "Email"

    const op = await obtenerDocentes();

        mostrarOpciones = ()=>{
            fragmento = document.createDocumentFragment();
            op.forEach(opcion =>{
                const opcionElemento = document.createElement("pre");
                opcionElemento.textContent = opcion;

    
                opcionElemento.addEventListener("click",()=> {
                    id.value = parseInt(opcion.substring(0,5));
                    nombre.value = opcion.substring(6,56).trimEnd();                   
                    apellido.value = opcion.substring(57, 107).trimEnd();
                    dni.value = opcion.substring(108,116);
                    email.value = opcion.substring(117, opcion.length)
                    eliminar.removeAttribute("hidden");
                });

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

                opcionElemento.addEventListener("click",()=> {
                    id.value = parseInt(opcion.substring(0,5));
                    nombre.value = opcion.substring(6,56).trimEnd();                   
                    apellido.value = opcion.substring(57, 107).trimEnd();
                    dni.value = opcion.substring(108,116);
                    email.value = opcion.substring(117, opcion.length)
                    eliminar.removeAttribute("hidden");
                });
    
                fragmento.appendChild(opcionElemento);

             });

             opciones.appendChild(fragmento);
          
        }
    }

    //Para darles estilos a los campos segun la validacion del backend
    erroresDadosPorBackend = ()=>{
        const errores = document.querySelectorAll(".error");

        //primero veo si hay erroes, porque ya que esto siempre se hace cunado se carga la pagina, puedo ni validar nada y ya se me estarian poniendo los campos como validos
        if(errores.length > 0){
            elementos = {"nombre":nombre,"apellido":apellido,"dni":dni,"email":email};
            //Si un error contiene el nombre de un campo entonces es invalido
            errores.forEach(error=>{
                if(error.textContent.includes("nombre")){
                    nombre.classList.add("is-invalid");
                    nombre.classList.remove("is-valid");
                    delete elementos["nombre"];
                }

                if(error.textContent.includes("apellido")){
                    apellido.classList.add("is-invalid");
                    apellido.classList.remove("is-valid");
                    delete elementos["apellido"];
                }

                if(error.textContent.toLowerCase().includes("dni")){
                    dni.classList.add("is-invalid");
                    dni.classList.remove("is-valid");
                    delete elementos["dni"];
                }

                if(error.textContent.includes("email")){
                    email.classList.add("is-invalid");
                    email.classList.remove("is-valid");
                    delete elementos["email"];
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

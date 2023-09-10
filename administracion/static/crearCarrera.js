const nombre = document.getElementById("nombre");
const duracion = document.getElementById("duracion");
const limpiar = document.getElementById("limpiar");
const id = document.getElementById("id");
const eliminar = document.getElementById("eliminar");
const enviar = document.getElementById("enviar");
const verAlumnos = document.getElementById("verAlumnos");


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
        duracion.focus();
    }
});

duracion.addEventListener("input",()=>{
    posicionDeComa = duracion.value.indexOf(".");
    if(posicionDeComa == -1){
        if(duracion.value.length > 2){
            duracion.value = duracion.value.substring(0,2);
        }
    }else{
        substring1 = duracion.value.substring(0,posicionDeComa);
        substring2 = duracion.value.substring(posicionDeComa,duracion.value.length+1);
        if(substring2.length > 3){
            duracion.value = substring1 + substring2.substring(0, 3)
        }
    }
});

limpiar.addEventListener("click",(e)=>{
    id.value = "";
    nombre.value = "";
    duracion.value = "";
    eliminar.setAttribute("hidden","");
    verAlumnos.setAttribute("hidden","");

    nombre.classList.remove("is-valid");
    nombre.classList.remove("is-invalid");

    duracion.classList.remove("is-valid");
    duracion.classList.remove("is-invalid");
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





const formatearCarrera = (carrera)=>{
    let carreraFormateada = carrera.id.toString().padStart(5,"0") + " " + carrera.nombre.padEnd(50," ") + " " + carrera.duracion.toFixed(2).toString().padStart(5," ");

    return carreraFormateada;
}

const obtenerCarreras = async () => {
    try{

        const respuesta = await fetch('/administracion/obtenerCarreras/');  // Cambia la URL según tu configuración
        const data = await respuesta.json();
        const carreras = data.map(carrera => formatearCarrera(carrera));
        return carreras;

    } catch (error) {
        console.error('Error al obtener las carreras:', error);
        return [];
    }
         
}

document.addEventListener("DOMContentLoaded", async () => {
    const busqueda = document.getElementById("busqueda");
    const opciones = document.getElementById("opciones");
    const pre = document.getElementById("pre");

    pre.textContent = "ID" + " ".repeat(4) + "Nombre" + " ".repeat(45) + "Duracion"

    // Ejemplo de opciones (aquí puedes cargar las opciones desde una fuente de datos externa)
    //obtenerCarreras devuelve una promesa asi que debo hacerle el then, pero si lo hago el resto de la funcion se ejecutara antes de terminar la promesa, entonces debo convertir toda esta funcion en una asyncrona para agregar un await, ademas ya que obtenerCarreras devuelve un arreglo, directo la respuesta va a ser un arreglo
    const op = await obtenerCarreras();

        mostrarOpciones = ()=>{
            fragmento = document.createDocumentFragment();
            op.forEach(opcion =>{
                const opcionElemento = document.createElement("pre");
                opcionElemento.textContent = opcion;

    
                opcionElemento.addEventListener("click",()=> {
                    id.value = parseInt(opcion.substring(0,5));
                    nombre.value = opcion.substring(6,57).trimEnd();                   
                    duracion.value = opcion.substring(58, opcion.length);
                    eliminar.removeAttribute("hidden");
                    verAlumnos.removeAttribute("hidden");
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
                    nombre.value = opcion.substring(6,57).trimEnd();                   
                    duracion.value = opcion.substring(58, opcion.length);
                    eliminar.removeAttribute("hidden");
                    verAlumnos.removeAttribute("hidden");
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
            elementos = {"nombre":nombre,"duracion":duracion};
            //Si un error contiene el nombre de un campo entonces es invalido
            errores.forEach(error=>{
                if(error.textContent.includes("nombre")){
                    nombre.classList.add("is-invalid");
                    nombre.classList.remove("is-valid");
                    delete elementos["nombre"];
                }

                if(error.textContent.includes("duracion")){
                    duracion.classList.add("is-invalid");
                    duracion.classList.remove("is-valid");
                    delete elementos["duracion"];
                }

                if(error.textContent.includes("Complete todos los campos")){
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
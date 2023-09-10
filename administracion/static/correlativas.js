const id = document.getElementById("id");
const bandera = document.getElementById("bandera");
const guardar = document.getElementById("guardar");

let correlativasCambiantes = [];

getCookie = (name)=>{
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

guardar.addEventListener("click",()=>{
    let ids = [];

    correlativasCambiantes.forEach(corre =>{
        if(corre.innerHTML[corre.innerHTML.length - 1] == "C"){
            ids.push(parseInt(corre.innerHTML.substring(0,5)));
        }
    });

    obj = {"id": id.innerHTML,"ids":ids}
    
    fetch('/administracion/guardarCorrelativas/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(obj)
      })
      //agrego este if, ya que al devolver en backend con esto JsonResponse, a pesar de que sabe que es un error, no lo toma como tal y va al catch si no va al then y lo toma como la data de retorno, por eso agregamos el if, asi si el response no es un ok, lanzo yo mismo un error y asi voy al catch
      .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error('Error en la solicitud: ' + errorData.error);
              });
          }
          return response.json();
      })
      .then(data => {
        alert(data["mensaje"]);
        bandera.setAttribute("hidden","");
      })
      .catch(error => {
        console.log('Error en la solicitud: ', error);
        alert(error.message); // Mostrar el mensaje de error personalizado
      });
});


const formatearCorrelativa = (correlativa)=>{
    let correlativaFormateada = correlativa.id.toString().padStart(5,"0") + " " + correlativa.nombre.padEnd(50," ") + " " + correlativa.es_correlativa;
    return correlativaFormateada;
}

const obtenerCorrelativas = async () => {
    try{
        respuesta = await fetch('/administracion/obtenerCorrelativas/' + id.innerHTML);  // 
        const data = await respuesta.json();
        const correlativa = data.map(correlativa => formatearCorrelativa(correlativa));        return correlativa;

    } catch (error) {
        console.error('Error al obtener los alumnos:', error);
        return [];
    }
         
}

document.addEventListener("DOMContentLoaded", async () => {
    const busqueda = document.getElementById("busqueda");
    const opciones = document.getElementById("opciones");
    const pre = document.getElementById("pre");

    pre.textContent = "ID" + " ".repeat(4) + "Nombre" + " ".repeat(45) + "Correlativa";

    const op = await obtenerCorrelativas();

        mostrarOpciones = ()=>{
            fragmento = document.createDocumentFragment();
            op.forEach(opcion =>{
                const opcionElemento = document.createElement("pre");
                opcionElemento.textContent = opcion;

                opcionElemento.addEventListener("dblclick",()=>{
                    if(opcionElemento.innerHTML[opcionElemento.innerHTML.length - 1] == " "){
                        opcionElemento.innerHTML = opcionElemento.innerHTML.slice(0,-1) + "C";
                    }else{
                        opcionElemento.innerHTML = opcionElemento.innerHTML.slice(0,-1) + " ";
                    }

                    bandera.removeAttribute("hidden");
                });

                correlativasCambiantes.push(opcionElemento)
                fragmento.appendChild(opcionElemento);
            });

            opciones.appendChild(fragmento);
        }
  
      mostrarOpciones();
  
    // Función para mostrar las opciones coincidentes en la lista
    mostrarOpcionesCoincidentes = (termino) => {
        opciones.innerHTML = ""; // Limpiar la lista antes de mostrar las opciones
        if(termino == ""){
            fragmento = document.createDocumentFragment();

            correlativasCambiantes.forEach(opcion =>{
                opcion.addEventListener("dblclick",()=>{
                    if(opcion.innerHTML[opcion.innerHTML.length - 1] == " "){
                        opcion.innerHTML = opcion.innerHTML.slice(0,-1) + "C";
                    }else{
                        opcion.innerHTML = opcion.innerHTML.slice(0,-1) + " ";
                    }

                    bandera.removeAttribute("hidden");
                });
                fragmento.appendChild(opcion);
            });

            opciones.appendChild(fragmento);
        }else{
            const opcionesCoincidentes = correlativasCambiantes.filter(opcion => opcion.innerHTML.toLowerCase().includes(termino.toLowerCase()));
            
            fragmento = document.createDocumentFragment();
            opcionesCoincidentes.forEach(opcion => {

                opcion.addEventListener("dblclick",()=>{
                    if(opcion.innerHTML[opcion.innerHTML.length - 1] == " "){
                        opcion.innerHTML = opcion.innerHTML.slice(0,-1) + "C";
                    }else{
                        opcion.innerHTML = opcion.innerHTML.slice(0,-1) + " ";
                    }

                    bandera.removeAttribute("hidden");
                });

                fragmento.appendChild(opcion);

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

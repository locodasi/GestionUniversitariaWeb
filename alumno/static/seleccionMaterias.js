document.addEventListener("DOMContentLoaded",()=>{
    const carrera = document.getElementById("carrera");
    //Le da el evento para ver las notas a los select y solo a los permitidos
    DarEventoDeVerNotas();
    //cad avez que cambia el select de carreras, pido las nuevas materias de esa carrera
    carrera.addEventListener("change",()=>{
        obtenerMaterias(carrera.value)
    })

    //Evento al cursar
    document.getElementById("cursar").addEventListener("click",(e)=>{
        const select = document.getElementById("materias");
        if(validarSeleccionados(select)){
            cursarMaterias(select);
        }      
        e.preventDefault();
    });

    //Evento al dejar
    document.getElementById("dejar").addEventListener("click",(e)=>{
        const select = document.getElementById("cursadas");
        if(validarSeleccionados(select)){
            dejarMaterias(select);
        }      
        e.preventDefault();
    });

});

validarSeleccionados = select =>{
    if(select.selectedOptions.length > 0){
        return true
    }else{
        return false
    }

}

//Funcion para hacer que las materias cursadas o aprobadas puedan ver sus notas
//Ya que la funcion esta sobre los selects y no sobre los option, no tengo que volver a llamar a la funcion cuando vacie los select
DarEventoDeVerNotas=()=>{
    const verNotas = document.querySelectorAll(".verNotas");
    verNotas.forEach(elemento => {
        elemento.addEventListener("dblclick",(e)=>{
            verNotasFuncion(elemento.value);
        })
    });
}

//Obtengo las materias de la carrera
obtenerMaterias = async (idCarrera)=>{
    try{

        
        //Al usar wait y axios ya esta desencapsulada
        let materias = await axios("/alumno/obtenerMateriasJson/" + idCarrera);

        //recorro todas las claves que me devulve
        for(dato in materias.data){
            const fragmento = document.createDocumentFragment();

            //Recorro el dato devuelto en la clave y le creo un elemento option y lo sumo al fregamento
            for(materia of materias.data[dato]){
                const option = document.createElement("OPTION");
                option.value = materia[0];
                option.innerHTML = materia[1];
                fragmento.appendChild(option);
            }

            //Obtengo el select, ya que su id es == a la clave puedo obtenerlo asi y no hacer 3 para cada select y hacerlo solo una vez asi
            const select = document.getElementById(dato);
            //Limpio antes de sumar los valores
            limpiarSelect(select);

            select.appendChild(fragmento);
        }
    }catch(e){
        //Si hubo un error, intentar pasar a una carrera que no existe o no esta anotado, recargo pagina
        location.reload();
    }
}

//funcion para limpiar select
limpiarSelect = (select)=>{
    select.innerHTML = "";
}

//Funcion para cursar materias
cursarMaterias = async (select)=>{
    let opcionesSeleccionadas = select.selectedOptions;
    let valores = "";
    for(opcion of opcionesSeleccionadas){
        valores += opcion.value + ",";
    }
    valores = valores.slice(0,-1);
    const carrera = document.getElementById("carrera");
    let obj = {"idCarrera":carrera.value,"ids":valores}

    axios.defaults.headers.common['X-CSRFToken'] = obtenerToken();

    try{
        await axios.post("cursarMaterias/",obj).then((res)=>console.log(res.data));
         //Intercambio de options entre selects
    }catch(e){
        //Si hubo un error, intentar pasar a una carrera que no existe o no esta anotado, recargo pagina
        location.reload();
    }

    intercambioDeMateriasConCursadas(select,document.getElementById("cursadas"))
}

//Funcion para dejar materias
dejarMaterias = async (select)=>{
    let opcionesSeleccionadas = select.selectedOptions;
    let valores = "";
    for(opcion of opcionesSeleccionadas){
        valores += opcion.value + ",";
    }
    valores = valores.slice(0,-1);
    const carrera = document.getElementById("carrera");
    let obj = {"idCarrera":carrera.value,"ids":valores}

    axios.defaults.headers.common['X-CSRFToken'] = obtenerToken();

    try{
        await axios.post("dejarMaterias/",obj).then((res)=>console.log(res.data));
         //Intercambio de options entre selects
    }catch(e){
        //Si hubo un error, intentar pasar a una carrera que no existe o no esta anotado, recargo pagina
        location.reload();
    }

    intercambioDeMateriasConCursadas(select,document.getElementById("materias"))
}

//Funcion que intercambia entre materias y cursadas, las opciones seleccionadas, tanto de un lado como al otro
intercambioDeMateriasConCursadas = (select,selectAlQuePAsar)=>{
    const fragmento = document.createDocumentFragment();
    //Primero tengo que invertirlo para que al cambiar de select uno, no me haga bajar al otro y por ende no se pase, osea yo tengo 0 y 1, muevo el 0 y haora el 1 ocupa el lugar del 0, pero el for va a ir a buscar al 1, al ver que no hay, se termina, y por ende un elemento no paso de select
    opcionesSeleccionadas = Array.from(select.selectedOptions).reverse();
    for(option of opcionesSeleccionadas){
        fragmento.appendChild(option)
    }

    selectAlQuePAsar.appendChild(fragmento);
    ordenarSelect(selectAlQuePAsar);
}

ordenarSelect = (select) =>{

    let options = Array.from(select.options);

    //esta ordeno options por comparacion, de menor a mayor
    options.sort((a, b) => { return parseInt(a.value) - parseInt(b.value)});
    //Borro el select
    select.innerHTML = "";

    let fragmento = document.createDocumentFragment();

    options.forEach(option => fragmento.appendChild(option));
    select.appendChild(fragmento);
    select.selectedIndex = -1;
}

obtenerToken = ()=> document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtener el token CSRF

const verNotasFuncion = (id) =>{
    url = "/alumno/verNotas/" + id;
    window.location.href = url;
}

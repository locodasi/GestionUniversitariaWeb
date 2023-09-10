const contras = document.querySelectorAll('.contraseña');
const botones = document.querySelectorAll('.mostrarContra');
const ojos = document.querySelectorAll('.iconoDeOjo');

const enviar = document.getElementById("enviar");

//Funcion para que lo botones puedan ver la contra de su respectivo input
botones.forEach((elemento,posicion)=>{
    elemento.addEventListener('click', ()=> {
        if (contras[posicion].type === 'password') {
            contras[posicion].type = 'text';
            ojos[posicion].classList.add('fa-eye');
            ojos[posicion].classList.remove('fa-eye-slash');
        } else {
            contras[posicion].type = 'password';
            ojos[posicion].classList.add('fa-eye-slash');
            ojos[posicion].classList.remove('fa-eye');
        }
    });
});

const remplazar = (elemento,atributo)=>{
    if(atributo == "is-valid"){
        elemento.classList.add("is-valid");
        elemento.classList.remove("is-invalid");
    }else{
        elemento.classList.add("is-invalid");
        elemento.classList.remove("is-valid");
    }
};


//Verificar que al menos los campos esten llenos
enviar.addEventListener("click",(e)=>{
    let flag = true;
    for(const contra of contras){
        if(contra.value == ""){
            remplazar(contra,"is-invalid");
            flag = false;
        }else{
            contra.classList.remove("is-valid");
            contra.classList.remove("is-invalid");
        }
    }


    if(!flag){
        e.preventDefault();
    }
});


document.addEventListener("DOMContentLoaded", () => {

    //Funcion para pasar de input con un enter, menos el ultimo para mandar el form
    for(let i = 0; i<contras.length-1;i++){
        contras[i].addEventListener("keydown",(event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                contras[i+1].focus();
            }
        });
    }
   
    erroresDadosPorBackend = ()=>{
        const errores = document.querySelectorAll(".error");

        //primero veo si hay erroes, porque ya que esto siempre se hace cunado se carga la pagina, puedo ni validar nada y ya se me estarian poniendo los campos como validos
        if(errores.length > 0){
            errores.forEach(error=>{
                if(error.textContent.includes("antigua")){
                    contras[0].classList.add("is-invalid");
                    contras[0].classList.remove("is-valid");
                }

                if(error.textContent.includes("nueva")){
                    contras[1].classList.add("is-invalid");
                    contras[1].classList.remove("is-valid");

                    contras[2].classList.add("is-invalid");
                    contras[2].classList.remove("is-valid");
                }

            })
                
        }

    }

    erroresDadosPorBackend();
});



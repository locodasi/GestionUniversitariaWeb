const id_password = document.getElementById('id_password');
const username = document.getElementById("id_username");
const inputs = [username,id_password];

const mostrarContra = document.getElementById('mostrarContra');
const iconoDeOjo = document.getElementById('iconoDeOjo');

const enviar = document.getElementById("enviar");

mostrarContra.addEventListener('click', ()=> {
    if (id_password.type === 'password') {
        id_password.type = 'text';
        iconoDeOjo.classList.add('fa-eye');
        iconoDeOjo.classList.remove('fa-eye-slash');
    } else {
        id_password.type = 'password';
        iconoDeOjo.classList.add('fa-eye-slash');
        iconoDeOjo.classList.remove('fa-eye');
    }
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


enviar.addEventListener("click",(e)=>{
    let flag = true;
    for(const input of inputs){
        if(input.value == ""){
            remplazar(input,"is-invalid");
            flag = false;
        }else{
            input.classList.remove("is-valid");
            input.classList.remove("is-invalid");
        }
    }


    if(!flag){
        e.preventDefault();
    }
});


document.addEventListener("DOMContentLoaded", () => {
    let p = document.getElementById("error");
    const username = document.getElementById("id_username");

    if(p.innerHTML == "Usario o contraseña incorrecta"){
        id_password.classList.add("is-invalid");
        username.classList.add("is-invalid");
    }

    for(let i = 0; i<inputs.length-1;i++){
        inputs[i].addEventListener("keydown",(event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                inputs[i+1].focus();
            }
        });
    }
   
});


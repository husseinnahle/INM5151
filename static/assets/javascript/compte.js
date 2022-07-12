


function edit(){
    const email = document.getElementById("email");
    const name = document.getElementById("name");
    const password = document.getElementById("password");
    const edit_button = document.getElementById("edit-button");
    
    if( edit_button.innerText == "Done") {
        email.contentEditable = false;
        name.contentEditable = false;
        password.contentEditable = false;
        email.style.backgroundColor =  "#5f8de3";
        name.style.backgroundColor =  "#5f8de3";
        password.style.backgroundColor =  "#5f8de3";
        edit_button.innerText ="Edit";
    }else{
        email.contentEditable = true;
        name.contentEditable = true;
        password.contentEditable = true;
        email.style.backgroundColor =  "white";
        name.style.backgroundColor =  "white";
        password.style.backgroundColor =  "white";
        edit_button.innerText ="Done";
    }
}


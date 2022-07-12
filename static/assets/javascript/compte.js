


function edit(){
    alert("test")
    const email = document.getElementById("email");
    const name = document.getElementById("name");
    const password = document.getElementById("password");
    const edit_button = document.getElementById("edit-button");
    
    if( edit_button.innerText == "Done") {
        email.contentEditable = false;
        name.contentEditable = false;
        password.contentEditable = false;
        paragraph.style.backgroundColor =  rgb(145, 146, 146);;
        edit_button.innerText ="Edit"
    }else{
        email.contentEditable = true;
        name.contentEditable = true;
        password.contentEditable = true;
        paragraph.style.backgroundColor = rgb(237, 248, 248);
        edit_button.innerText ="Done"
    }
}


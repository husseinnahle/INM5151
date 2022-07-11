


function edit(){
    const paragraph = document.getElementById("edit");
    const edit_button = document.getElementById("edit-button");
    
    if( edit_button.innerText == "Done") {
        paragraph.contentEditable = false;
        paragraph.style.backgroundColor = "#ffe44d";
        edit_button.innerText ="Edit"
    }else{
        paragraph.contentEditable = true;
        paragraph.style.backgroundColor = "#dddbdb";
        edit_button.innerText ="Done"
    }
}


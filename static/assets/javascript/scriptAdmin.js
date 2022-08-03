$(document).ready(function(){
    $(".add-row").click(function(){
        document.getElementById("errorField").innerText = "";
        var Username = $("#Username").val();
        var Password = $("#password").val();
        var Email = $("#Email").val();
        var Type = $("#Type").val();
        // var Status = $("#Status").val();
        fetch('/api/admin/compte/ajouter?username=' + Username + "&password=" + Password + "&email=" + Email + "&type=" + Type)
        .then(function (response) {
          return response.text();
        }).then(function (text) {
            var jsonObject = JSON.parse(text);
            if (jsonObject["valid"] == false) {
                document.getElementById("errorField").innerText = jsonObject["reason"];
                return
            }
            var markup = `
                <tr id ="${jsonObject["id"]}">
                    <td><input type="checkbox" name="record"></td>
                    <td scope="row"id ="id" >${jsonObject["id"]}</td>
                    <td scope="row"id="name">${Username}</td>
                    <td id="email">${Email}</td>
                    <td id="type">${Type}</td>
                    <td id="type">active</td>
                    <td> <button type="button" class="edit-row" id="editBtn">Edit</button></td>
                    <td> <button type="button" class="delete-row" id="dltBtn">Delete</button></td>
                </tr>`;
            $("table tbody").append(markup);
        })
    });
    
    // Find and remove selected table rows
    $(".delete-rows").click(function(){
        $("table tbody").find('input[name="record"]').each(function(){
            if($(this).is(":checked")){
                var id =$(this).parents("tr").attr("id");
                fetch('/api/admin/compte/supprimer?id=' + id)
                .then(function (response) {
                    return response.text();
                })
                $(this).parents("tr").remove();
            }
        });
    });

     // Find and remove selected table rows
     $(".delete-row").click(function(){
        var id =$(this).parents("tr").attr("id");
        fetch('/api/admin/compte/supprimer?id=' + id)
        .then(function (response) {
          return response.text();
        })
        $(this).parents("tr").remove(); 
    });
});
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabContent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tabcontent.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  }
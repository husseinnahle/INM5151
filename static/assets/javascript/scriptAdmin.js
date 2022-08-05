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
  document.getElementById("add-action").style.display = "none";
  document.getElementsByClassName("account")[0].innerText = "Account";
}

function toggleRow(el) {
  el.classList.toggle("selected");
  el.classList.toggle("table-light");
}
  
function chooseAction(action) {
  var action_elements = document.getElementsByClassName("action");
  for (var i = 0; i < action_elements.length; i++) {
    action_elements[i].style.display = "none";
  }
  var elements = document.getElementsByClassName(action);
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = "block";
  }
  document.getElementsByClassName("account")[0].innerText = "Account | " + action.charAt(0).toUpperCase() + action.slice(1);
  if (action == "add") {
    document.getElementById('view').style.display = 'none';
  } else {
    document.getElementById('view').style.display = '';
  }
}

function addUser() {
  var username = document.getElementById('username').value;
  var email = document.getElementById('email').value;
  var password = document.getElementById('password').value;
  var type = document.getElementById('type').value;
  fetch('/api/admin/compte/ajouter?username=' + username + "&password=" + password + "&email=" + email + "&type=" + type)
    .then(function (response) {
      return response.text();
    }).then(function (text) {
      var jsonObject = JSON.parse(text);
      if (jsonObject["valid"] == false) {
          document.getElementById("form-popup-error-container").innerText = jsonObject["reason"];
          return
      }
      var markup = `
          <tr id="${jsonObject['id']}" href="#${jsonObject['id']}" onclick="toggleRow(this)">
            <td scope="row">${jsonObject['id']}</td>
            <td scope="row">${username}</td>
            <td scope="row">${email}</td>
            <td scope="row" id="type">${type}</td>
            <td scope="row" class="action edit" style="display:none">
                <select name="type" id="Type">
                    <option value="">--Choose a type--</option>
                    <option value="ADMIN">Administrator</option>
                    <option value="INSTRUCTOR">Instructor</option>
                    <option value="MEMBER">Member</option>
                    <option value="STANDARD">Standard</option>
                    <option value="{{user.type}}" id="previous_option" style="display:none"></option>
                </select>
                <button onclick="editRow('${jsonObject['id']}')">Done</button>
                <button onclick="cancelEditRow('${jsonObject['id']}')">Cancel</button>
            </td>
            <td scope="row" class="action delete" style="display:none"><button onclick="deleteRow('${jsonObject['id']}')">Delete</button></td>
          </tr>`;
      document.getElementById('view-body').innerHTML += markup;
      username.value = '';
      password.value = '';
      email.value = '';
      type.value = '';
      chooseAction('view');
      document.getElementById(jsonObject['id']).scrollIntoView({behavior: 'smooth'});
  })
}

function deleteUser(id) {
  document.getElementById(id).remove();
  fetch('/api/admin/compte/supprimer?id=' + id)
    .then(function (response) {
      return response.text();
  })
}
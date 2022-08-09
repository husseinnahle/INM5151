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
  document.getElementById("add-account").style.display = "none";
  document.getElementsByClassName("account")[0].innerText = "Account";
}

function toggleRow(el, exception) {
  if (document.getElementById("action").innerText != "delete" && exception == "false") {
    return;
  }
  el.classList.toggle("selected");
  el.classList.toggle("table-light");
}
  
function chooseAction(action) {
  document.querySelectorAll(".selected").forEach(el => toggleRow(el, 'true'));
  document.getElementById("action").innerText = action;
  var action_elements = document.getElementsByClassName("action");
  for (var i = 0; i < action_elements.length; i++) {
    action_elements[i].style.display = "none";
  }
  var elements = document.getElementsByClassName(action);
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = "";
  }
  document.getElementsByClassName("account")[0].innerText = "Account | " + action.charAt(0).toUpperCase() + action.slice(1);
  if (action == "add") {
    document.getElementById('view').style.display = 'none';
  } else {
    document.getElementById('view').style.display = '';
  }
  if (action == "edit") {
    document.querySelectorAll(".typeCell").forEach(el => el.style.display = 'none');
  } else {
    document.querySelectorAll(".typeCell").forEach(el => el.style.display = '');
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
          <tr id="${jsonObject["id"]}" onclick="toggleRow(this, 'false')">
          <td scope="row">${jsonObject["id"]}</td>
          <td scope="row">${username}</td>
          <td scope="row">${email}</td>
          <td scope="row" class="typeCell ${jsonObject["id"]}">${type}</td>
          <td scope="row" class="action edit" style="display:none">
              <select name="type" id="type" onchange="editUser(${jsonObject["id"]}, this)">
                  <option value="">${type}</option>
                  <option value="ADMIN">ADMIN</option>
                  <option value="INSTRUCTOR">INSTRUCTOR</option>
                  <option value="MEMBER">MEMBER</option>
                  <option value="STANDARD">STANDARD</option>
              </select>
          </td>
      </tr>`;
      document.getElementById('view-body').innerHTML += markup;
      document.querySelectorAll('.reset').forEach(el => el.value = '');
      chooseAction('view');
      document.getElementById(jsonObject['id']).scrollIntoView({behavior: 'smooth'});
  })
}

async function deleteUser() {
  var row = document.getElementsByClassName('selected');
  var urls = [];
  for (var i = 0; i < row.length; i++) {
    var user_id = row[i].id;
    urls.push('/api/admin/compte/supprimer?id=' + user_id);
  }
  document.querySelectorAll(".selected").forEach(el => el.remove());
  (async () => {
    try {
      const requests = urls.map((url) => fetch(url));
      await Promise.all(requests);
    }
    catch (errors) {
      errors.forEach((error) => console.error(error));
    }
  })();
}

async function editUser(id, el) {
  await fetch('/api/admin/compte/modifier?id=' + id + '&type=' + el.value);
  document.getElementsByClassName("typeCell "+id)[0].innerText = el.value;
}

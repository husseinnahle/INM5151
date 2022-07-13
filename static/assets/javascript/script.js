var reponses = [];

function questionSuivante() {
  document.getElementById('erreur').innerHTML = '';
  var checked = enregistrerReponse();
  if(checked == false) {
    document.getElementById('erreur').innerText = 'Choisissez une réponse!';
    return true;
  }
  var sujet = document.getElementById('sujet').innerText;
  var sous_sujet = document.getElementById('sous_sujet').innerText;
  var numero = document.getElementById('numero').innerText;
  chercherQuestion(sujet, sous_sujet, numero);
  return true;
}

function chercherQuestion(sujet, sous_sujet, numero_str) {
  fetch('/api/quiz?sujet=' + sujet + '&sous-sujet=' + sous_sujet + '&numero=' + numero_str)
		.then(function(response) {
      if(response.status = 200) {
        return response.text();
      }
		}).then(function(text) {
			var jsonObject = JSON.parse(text);
      var numero = +numero_str;
      numero++; 
      modifierQuestion(numero.toString(), jsonObject["Question"], jsonObject["Choix"]);
		}).catch(err => post(sujet, sous_sujet));
}

function modifierQuestion(numero, question, choix) {
  document.getElementById('numero').innerText = numero;
  document.getElementById('question').innerText = question;
  document.getElementById("container").innerHTML = "";
  for(var i = 0; i < choix.length; i++) {
    document.getElementById("container").innerHTML += `<input type="radio" id="choix" name="choix">
    <label id="choix" name="choix_label" for=${choix[i]}>${choix[i]}</label><br>`;
  }
}

function enregistrerReponse() {
  var input = document.getElementsByName('choix');
  var label = document.getElementsByName('choix_label');
  for(var i = 0; i < input.length; i++) {
    if(input[i].checked) {
      reponses.push(label[i].innerText);
      input[i].checked = false;
      return true;
    }
  }
  return false;
}

function post(sujet, sous_sujet) {
  const form = document.createElement('form');
  form.method = "POST";
  form.action = "/languages/quiz/resultat";
  const hiddenField = document.createElement('input');
  hiddenField.type = 'hidden';
  hiddenField.name = "data";
  var data = {
    "sujet": sujet,
    "sous-sujet": sous_sujet,
    "reponses": reponses 
  }
  hiddenField.value = JSON.stringify(data);
  form.appendChild(hiddenField);
  document.body.appendChild(form);
  form.submit();
}

function addArrows() {
  var nodes = document.getElementsByClassName("node");
  for (var i = 0; i < nodes.length; i++) {
    if (i+1 < nodes.length) {
      endPlug = 'behind';
      _dash = null;
      if (nodes[i].getAttribute("name") == "done" && nodes[i+1].getAttribute("name") == "current") {
        endPlug = 'hand';
        _dash = {animation: true};
      } else if (nodes[i].getAttribute("name") == "done" && nodes[i+1].getAttribute("name") == "done") {
        continue;
      }
      new LeaderLine (
        document.getElementById(nodes[i].id),
        document.getElementById(nodes[i+1].id),
        {
          endPlug: endPlug,
          endPlugSize: 0.9,
          color: "black",
          dash: _dash
        }
      );
    }
  }
}

function openPopup() {
  document.getElementById("popup").classList.add("open-popup");
  document.getElementById("tree-container").style.pointerEvents = "none";
  document.getElementById("tree-container").style.filter = "blur(10px)";
  var arrows = document.getElementsByClassName("leader-line");
  for(var i = 0; i < arrows.length; i++){
    arrows[i].style.filter = "blur(10px)";
  }
}

function is_authorized(){
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  fetch('/api/is_authorized?username=' + username + '&password=' + password + '&path=' + window.location.pathname)
  .then(function(response) {
    return response.text();
  }).then(function(text) {
    var response = JSON.parse(text);
    if (response["is_authorized"] == false) {
      document.getElementById("form-popup-error-container").innerHTML = `<span id="form-popup-error">${response["reason"]}</span><br>`;
    } else {
      document.getElementById("form-popup").submit();
    }
  });
  return true;
}

function edit_input(){
  var input = document.getElementsByTagName("input");
  var edit_button = document.getElementById("edit");
  
  if ( edit_button.innerText == "Edit") {
      for(var i = 0; i < input.length; i++) {
        input[i].readOnly = false;
        input[i].style.cursor = "text";
        input[i].style.background = "#e4e4e4";
        input[i].style.color = "#2d3033";  
      }
      edit_button.innerText ="Done";
      edit_button.style.color = "#f83470";
      edit_button.style.backgroundColor = "#2d3033";
      edit_button.style.border = "2px solid #f83470";
  } else {
    for(var i = 0; i < input.length; i++) {
      input[i].readOnly = true;
      input[i].style.cursor = "default";
      input[i].style.background = "#2d3033";
      input[i].style.color = "#e4e4e4";  
    }
    edit_button.innerText ="Edit";
    edit_button.style.color = "#e4e4e4";
    edit_button.style.backgroundColor = "#f83470";
    edit_button.style.border = "0";
  }
}

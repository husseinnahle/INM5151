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

function setTree() {
  const position_left = ["-150px", "150px", "-200px", "-80px", "220px", "150px", "-200px"];
  const position_top = ["5px", "80px", "-10px", "110px", "-150px", "0px", "-100px"];
  const nodes = document.getElementsByClassName("node");
  for (var i = 0; i < nodes.length; i++) {
    nodes[i].style.left = position_left[i%7];
    nodes[i].style.top = position_top[i%7];
  }
  addArrows(nodes);
  document.getElementById("tree").style.visibility = "visible";
  return true;
}

function addArrows(nodes) {
  for (var i = 0; i < nodes.length; i++) {
    if (i+1 < nodes.length) {
      new LeaderLine (
        document.getElementById(nodes[i].id),
        document.getElementById(nodes[i+1].id),
        {
          color: "black",
          dash: {animation: true}  // Optionelle
        }
      );
    }
  }
}

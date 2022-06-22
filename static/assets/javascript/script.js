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
  var label = document.getElementsByName('choix_label');
  for(var i = 0; i < label.length; i++) {
    label[i].innerText = choix[i];
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
  form.action = "/tutoriels/quiz/resultat";
  const hiddenField = document.createElement('input');
  hiddenField.type = 'hidden';
  hiddenField.name = "data";
  var data = {
    "Sujet": sujet,
    "Sous-sujet": sous_sujet,
    "Reponses": reponses 
  }
  hiddenField.value = JSON.stringify(data);
  form.appendChild(hiddenField);
  document.body.appendChild(form);
  form.submit();
}
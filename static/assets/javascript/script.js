var reponses = [];
//quiz
function questionSuivante() {
  document.getElementById('erreur').innerHTML = '';
  var checked = enregistrerReponse();
  if (checked == false) {
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
    .then(function (response) {
      if (response.status = 200) {
        return response.text();
      }
    }).then(function (text) {
      var jsonObject = JSON.parse(text);
      var numero = +numero_str;
      numero++;
      modifierQuestion(numero.toString(), jsonObject["Question"], jsonObject["Choix"]);
    }).catch(err => post(sujet, sous_sujet));
}

function modifierQuestion(numero, question, choix) {
  document.getElementById('numero').innerText = numero;
  document.getElementById('question').innerText = question;
  document.getElementById("quiz-choix").innerHTML = "";
  for (var i = 0; i < choix.length; i++) {
    document.getElementById("quiz-choix").innerHTML += `<label><input type="radio" id="choix" name="choix"/><span id="choix" name="choix_label" for=${choix[i]}>${choix[i]}</span></label>`;
  }
}

function enregistrerReponse() {
  var input = document.getElementsByName('choix');
  var label = document.getElementsByName('choix_label');
  for (var i = 0; i < input.length; i++) {
    if (input[i].checked) {
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
//END QUIZ
function addArrows() {
  var nodes = document.getElementsByClassName("node");
  for (var i = 0; i < nodes.length; i++) {
    if (i + 1 < nodes.length) {
      endPlug = 'behind';
      _dash = null;
      if (nodes[i].getAttribute("name") == "done" && nodes[i + 1].getAttribute("name") == "current") {
        endPlug = 'hand';
        _dash = { animation: true };
      } else if (nodes[i].getAttribute("name") == "done" && nodes[i + 1].getAttribute("name") == "done") {
        // continue;
      }
      new LeaderLine(
        document.getElementById(nodes[i].id),
        document.getElementById(nodes[i + 1].id),
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
  for (var i = 0; i < arrows.length; i++) {
    arrows[i].style.filter = "blur(10px)";
  }
}

function is_authorized(pathname) {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  fetch('/api/is_authorized?username=' + username + '&password=' + password + '&path=' + pathname)
    .then(function (response) {
      return response.text();
    }).then(function (text) {
      var response = JSON.parse(text);
      if (response["is_authorized"] == false) {
        document.getElementById("form-popup-error-container").innerHTML = `<span id="form-popup-error">${response["reason"]}</span><br>`;
        hcaptcha.reset()
      } else {
        document.getElementById("form-popup").submit();
      }
    });
  return true;
}

function editInput() {
  var input = document.getElementsByTagName("input");
  var edit_button = document.getElementById("edit");
  document.getElementById("message").innerText = "";
  if (edit_button.innerText == "Edit") {
    for (var i = 0; i < input.length; i++) {
      enableField(input[i]);
    }
    document.getElementById("cancel").style.visibility = "visible";
    edit_button.innerText = "Done";
    edit_button.style.color = "#f83470";
    edit_button.style.backgroundColor = "#2d3033";
  } else {
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var url = '/api/compte/modifier?username=' + username + '&password=' + password + '&email=' + email;
    if (username == "" || email == "" || password == "") {
      document.getElementById("message").innerText = "All fields are required!";
      document.getElementById("message").style.color = 'red';
      return;
    } else if (password == "********") {
      url = '/api/compte/modifier?username=' + username + '&email=' + email;
    }
    fetch(url)
      .then(function (response) {
        if (response.status = 200) {
          return response.text();
        }
      }).then(function (text) {
        var response = JSON.parse(text);
        if (response["valid"] == false) {
          document.getElementById("message").innerText = response["reason"];
          document.getElementById("message").style.color = 'red';
          return;
        }
        document.getElementById("cancel").style.visibility = "hidden";
        document.getElementById("message").innerText = "Account info updated!";
        document.getElementById("message").style.color = 'white';
        document.getElementById("navbarDarkDropdownMenuLink").innerText = username;
        for (var i = 0; i < input.length; i++) {
          disableField(input[i]);
        }
        edit_button.innerText = "Edit";
        edit_button.style.color = "#e4e4e4";
        edit_button.style.backgroundColor = "#f83470";
      });
  }
}

function cancelEdit() {
  document.getElementById("cancel").style.visibility = "hidden";
  var input = document.getElementsByTagName("input");
  var edit_button = document.getElementById("edit");
  var username = document.getElementById("username");
  var email = document.getElementById("email");
  var password = document.getElementById("password");
  username.value = username.className;
  email.value = email.className;
  password.value = password.className;
  edit_button.innerText = "Edit";
  edit_button.style.color = "#e4e4e4";
  edit_button.style.backgroundColor = "#f83470";
  for (var i = 0; i < input.length; i++) {
    disableField(input[i]);
  }
}

function enableField(input) {
  input.readOnly = false;
  input.style.cursor = "text";
  input.style.background = "#e4e4e4";
  input.style.color = "#2d3033";
}

function disableField(input) {
  input.readOnly = true;
  input.style.cursor = "default";
  input.style.background = "#2d3033";
  input.style.color = "#e4e4e4";
}

function clearField() {
  var password = document.getElementById("password");
  if (password.readOnly == true) {
    return;
  }
  password.value = "";
}

function closeAd() {
  document.getElementById("publicite-popup").remove();
  document.getElementById("quiz-container").style.filter = "blur(0px)";
  document.getElementById("quiz-container").style.pointerEvents = "all";
}

function showSkip() {
  document.getElementById("skip").style.visibility = "visible";
}

function paiement() {
  fetch("/config")
  .then((result) => { return result.json(); })
  .then((data) => {
    const stripe = Stripe(data.publicKey);
    document.querySelector("#submitBtn").addEventListener("click", () => {
      document.getElementById("paiement-button-container").innerHTML=`<div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div>`;
      fetch("/create-checkout-session")
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);     
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  });
}
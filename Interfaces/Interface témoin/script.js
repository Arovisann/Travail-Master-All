
// Fonction pour valider l'adresse e-mail
function validateEmail(email) {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Regex pour valider une adresse e-mail
  return emailPattern.test(email) ? "" : "Veuillez entrer une adresse e-mail valide.";
}

// Fonction pour valider le mot de passe
function validatePassword(password) {
  const minLength = /.{8,}/;
  const uppercase = /[A-Z]/;
  const lowercase = /[a-z]/;
  const digitOrSpecial = /[\d\W]/;

  if (!minLength.test(password)) {
    return "Le mot de passe doit contenir au moins 8 caractères.";
  }
  if (!uppercase.test(password)) {
    return "Le mot de passe doit contenir au moins une majuscule.";
  }
  if (!lowercase.test(password)) {
    return "Le mot de passe doit contenir au moins une minuscule.";
  }
  if (!digitOrSpecial.test(password)) {
    return "Le mot de passe doit contenir un chiffre ou un caractère spécial.";
  }
  return ""; // Mot de passe valide
}

function validateGender() {
  const monsieur = document.getElementById("monsieur").checked;
  const madame = document.getElementById("madame").checked;

  if (!monsieur && !madame) {
    return false; // Aucun choix sélectionné
  }
  return monsieur ? "Monsieur" : "Madame";
}

// Fonction pour valider les champs nom et prénom
function validateNameField(value, fieldName) {
  if (!value || !/^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$/.test(value)) {
    alert(`Veuillez entrer un ${fieldName} valide.`);
    return false;
  }
  return true;
}
// Fonction pour valider un numéro (ex: numéro de rue)
function validateNumberField(value, fieldName) {
  if (!value || !/^\d+$/.test(value)) {
    alert(`Veuillez entrer un ${fieldName} valide (uniquement des chiffres).`);
    return false;
  }
  return true;
}

// Fonction pour valider les conditions générales (obligatoire)
function validateConditions() {
  const conditionsChecked = document.getElementById("conditions").checked;
  if (!conditionsChecked) {
    alert("Vous devez accepter les conditions générales pour continuer.");
    return false;
  }
  return true;
}

// Fonction pour sauvegarder des données dans le localStorage
function saveToLocalStorage(key, value) {
  localStorage.setItem(key, value);
}

// Fonction pour réinitialiser le localStorage
function resetLocalStorage() {
  localStorage.clear();
  alert("Données réinitialisées !");
}

// Fonction pour gérer la soumission du formulaire
function handleFormSubmit(event) {
  event.preventDefault(); // Empêche l'envoi du formulaire

  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const errorMessage = document.getElementById("error-message");
  const prenomInput = document.getElementById('prenom');
  const nomInput = document.getElementById('nom');
  const rueInput = document.getElementById('rue');
  const codeInput = document.getElementById("code");
  const localiteInput = document.getElementById('localite');
  const paysInput = document.getElementById('pays');
  const phoneInput = document.getElementById("phone");
  const jourInput = document.getElementById("jour");
  const moisInput = document.getElementById("mois");
  const ansInput = document.getElementById("ans");

  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();
  const gender = validateGender();
  const prenom = prenomInput.value.trim();
  const nom = nomInput.value.trim();
  const rue = rueInput.value.trim();
  const code = codeInput.value.trim();
  const localite = localiteInput.value.trim();
  const pays = paysInput.value.trim();
  const phone = phoneInput.value.trim();
  const jour = jourInput.value.trim();
  const mois = moisInput.value.trim();
  const ans = ansInput.value.trim();

  let formIsValid = true;
  errorMessage.style.display = "none"; // Masquer les messages d'erreur précédents

  // Validation email
  const emailError = validateEmail(email);
  if (emailError) {
    errorMessage.textContent = emailError;
    errorMessage.style.display = "block";
    formIsValid = false;
  }

  // Validation mot de passe
  const passwordError = validatePassword(password);
  if (passwordError) {
    errorMessage.textContent = passwordError;
    errorMessage.style.display = "block";
    formIsValid = false;
  }

  // Validation genre
  if (!gender) {
    errorMessage.textContent = "Veuillez sélectionner Monsieur ou Madame.";
    errorMessage.style.display = "block";
    formIsValid = false;
  }

  // Autres validations
  if (!validateNameField(prenom, "prénom")) formIsValid = false;
  if (!validateNameField(nom, "nom")) formIsValid = false;
  if (!validateNameField(rue, "rue")) formIsValid = false;
  if (!validateNumberField(code, "code")) formIsValid = false;
  if (!validateNameField(localite, "localité")) formIsValid = false;
  if (!validateNameField(pays, "pays")) formIsValid = false;
  if (!validateNumberField(phone, "numéro de téléphone")) formIsValid = false;
  if (!validateNumberField(jour, "jour de naissance")) formIsValid = false;
  if (!validateNumberField(mois, "mois de naissance")) formIsValid = false;
  if (!validateNumberField(ans, "année de naissance")) formIsValid = false;
  if (!validateConditions()) formIsValid = false;

  if (!formIsValid) return; // Arrêter ici si une validation a échoué

  // Si tout est valide, on sauvegarde dans le localStorage
  saveToLocalStorage("userEmail", email);
  saveToLocalStorage("userPassword", password);
  saveToLocalStorage("userGender", gender);
  saveToLocalStorage('userPrenom', prenom);
  saveToLocalStorage('userNom', nom);
  saveToLocalStorage("userCode", code);
  saveToLocalStorage("userLocalite", localite);
  saveToLocalStorage("userPays", pays);
  saveToLocalStorage("userPhone", phone);
  saveToLocalStorage("userJour", jour);
  saveToLocalStorage("userMois", mois);
  saveToLocalStorage("userAns", ans);

  saveToLocalStorage("loggedIn", "false");
  saveToLocalStorage("currentUser", email);
  saveToLocalStorage("formValidated", "true");
  
    // --- CheckFlag C ---
  const startTime = localStorage.getItem("experienceStartTime");

  if (startTime) {
    const now = Date.now();
    const elapsed = ((now - startTime) / 1000).toFixed(2);
    localStorage.setItem("CheckFlagC", elapsed);
    console.log("✅ CheckFlag C enregistré : " + elapsed + " secondes");
  }

  



  window.location.href = "../index/index.html";
}



// Initialisation des événements
function initializeApp() {
  const form = document.getElementById("signup-form");
  const resetButton = document.getElementById("reset-button");

  if (form) {
    form.addEventListener("submit", handleFormSubmit);
  }

  if (resetButton) {
    resetButton.addEventListener("click", resetLocalStorage);
  }
}



// Appeler la fonction d'initialisation au chargement de la page
document.addEventListener("DOMContentLoaded", initializeApp);

// Fonction pour gérer la connexion
function handleLogin(event) {
  event.preventDefault(); // Empêche le rechargement de la page

  console.log("Bouton de connexion cliqué !"); // Vérifier si la fonction se lance

  const emailInput = document.getElementById("login-email").value.trim();
  const passwordInput = document.getElementById("login-password").value.trim();
  const errorMessage = document.getElementById("login-error");

  // Vérification de la récupération des valeurs
  console.log("Email saisi :", emailInput);
  console.log("Mot de passe saisi :", passwordInput);

  // Récupérer les données du localStorage
  const storedEmail = localStorage.getItem("userEmail");
  const storedPassword = localStorage.getItem("userPassword");

  console.log("Email stocké :", storedEmail);
  console.log("Mot de passe stocké :", storedPassword);

  // Vérifier si les champs sont remplis
  if (!emailInput || !passwordInput) {
      errorMessage.textContent = "Veuillez remplir tous les champs.";
      errorMessage.style.display = "block";
      return;
  }

  // Vérifier si l'email et le mot de passe correspondent
  if (emailInput === storedEmail && passwordInput === storedPassword) {
      errorMessage.style.display = "none"; // Cacher les erreurs
      console.log("Connexion réussie ! Redirection...");
      saveToLocalStorage("loggedIn", "true");

      // ✅ Rediriger vers la page d'accueil
      window.location.href = "../index/index.html";
  } else {
      console.log("Échec de la connexion !");
      errorMessage.textContent = "Adresse e-mail ou mot de passe incorrect.";
      errorMessage.style.display = "block";
  }
}

// Attacher l'événement au bouton de connexion
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM chargé, ajout de l'écouteur d'événement...");
  document.getElementById("login-button").addEventListener("click", handleLogin);
});

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.querySelector(".search-input"); // Sélectionne le champ de recherche
  const searchButton = document.querySelector(".search-button"); // Sélectionne le bouton de recherche

  function performSearch() {
    const query = searchInput.value.trim().toLowerCase();

    if (query === "parasol") {
      window.location.href = "../frame 12/index.html";
    } else if (query === "suncomfort by glatz") {
      window.location.href = "../frame 10/index.html";
    } else {
      window.location.href = "../frame 11/index.html";
    }
  }

  // Détection de la touche "Entrée" dans la barre de recherche
  searchInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      performSearch();
    }
  });

  // Détection du clic sur le bouton de recherche
  searchButton.addEventListener("click", function () {
    performSearch();
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const addToCartButton = document.getElementById("add-to-cart");
if (addToCartButton) {
  addToCartButton.addEventListener("click", function () {
    console.log("Bouton 'Ajouter au panier' cliqué !"); // Vérification
    
    const item = {
      name: "SUNCOMFORT BY GLATZ Siesta Mât central (180 cm x 130 cm, Rouge)",
      price: "CHF 49.-",
      image: "https://c.animaapp.com/vYefCoeT/img/component-1-19.svg"
    };

    localStorage.setItem("cartItem", JSON.stringify(item));
    console.log("Article ajouté au localStorage :", localStorage.getItem("cartItem")); // Vérification

    alert("✅ Le produit a bien été ajouté au panier !");
    window.location.href = "../index/index.html"; // Redirige vers le panier
  });
} else {
  console.log("⚠️ Bouton 'Ajouter au panier' non trouvé !");
}

  const cartContainer = document.querySelector(".panierachat");

  if (cartContainer) {
    const cartItem = localStorage.getItem("cartItem");
    const user = localStorage.getItem("loggedIn") === "true";; // Vérifie si l'utilisateur est connecté

    if (cartItem) {
      const item = JSON.parse(cartItem);

      cartContainer.innerHTML = `
        <div class="cart-item">
          <img src="${item.image}" alt="${item.name}" class="cart-item-image">
          <div class="cart-item-details">
            <p class="cart-item-name">${item.name}</p>
            <p class="cart-item-price">${item.price}</p>
            <button id="remove-from-cart">Supprimer</button>
          </div>
        </div>
        <div class="cart-actions">
          <button id="auth-button">${user ? "Valider le panier" : "Se connecter"}</button>
        </div>
      `;

      // Supprimer l'article du panier
      document.getElementById("remove-from-cart").addEventListener("click", function () {
        localStorage.removeItem("cartItem");
        location.reload();
      });

      // Bouton Connexion ou Validation
      document.getElementById("auth-button").addEventListener("click", function () {
        const buttonText = this.textContent.trim();
        const startTime = localStorage.getItem("experienceStartTime");

        if (startTime) {
          const now = Date.now();
          const elapsed = ((now - startTime) / 1000).toFixed(2);

          if (buttonText === "Se connecter") {
            if (!localStorage.getItem("FlagB")) {
              localStorage.setItem("FlagB", elapsed);
              console.log("✅ CheckFlag B enregistré : " + elapsed + " secondes");
            } else {
              console.log("⏩ CheckFlag B déjà enregistré, aucune mise à jour.");
            }
            window.location.href = "../frame 9/index.html";
          } else if (buttonText === "Valider le panier") {
            localStorage.setItem("checkFlagFinal", elapsed);
            console.log("✅ CheckFlag Final enregistré : " + elapsed + " secondes");
            alert("Votre commande a été validée !");
            localStorage.removeItem("cartItem");
            location.reload();
          }

        } else {
          console.warn("⛔ Timer de l'expérience non démarré !");
        }
      });
    }
  }
});


// counter.js

// Attendre que le DOM soit complètement chargé avant d'exécuter le code
document.addEventListener('DOMContentLoaded', function() {
  // Récupérer le nombre de clics total dans localStorage, sinon initialiser à 0
  let totalClickCount = localStorage.getItem('totalClickCount') ? parseInt(localStorage.getItem('totalClickCount')) : 0;

  // Fonction pour incrémenter le compteur de clics
  function incrementClickCount() {
      totalClickCount++;
      localStorage.setItem('totalClickCount', totalClickCount);  // Sauvegarder le compteur dans localStorage
      console.log(`Total de clics : ${totalClickCount}`);
  }

  // Ajouter un écouteur d'événement sur tout le document pour les clics
  document.addEventListener('click', incrementClickCount);
});








document.addEventListener("DOMContentLoaded", function () {
  // Lenteur sur les liens <a>
  document.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      const shouldDelay = Math.random() < 0.7; // 70% de chance d'avoir un retard
      const shouldIgnore = Math.random() < 0.3; // 30% de chance que le clic ne fonctionne pas

      if (shouldIgnore) {
        alert("Une erreur est survenue. Veuillez réessayer.");
      } else if (shouldDelay) {
        setTimeout(() => {
          window.location.href = link.href;
        }, 4000); // 4 secondes de retard
      } else {
        window.location.href = link.href;
      }
    });
  });

  // Boutons capricieux
  document.querySelectorAll("button").forEach(button => {
    button.addEventListener("click", function () {
      if (Math.random() < 0.4) {
        alert("Une erreur inconnue est survenue. Réessayez.");
      }
    });
  });

  // Suppression aléatoire des champs de formulaire après saisie
  document.querySelectorAll("input, textarea").forEach(input => {
    input.addEventListener("blur", function () {
      if (Math.random() < 0.3) {
        this.value = "";
        alert("Votre saisie a été effacée. Veuillez recommencer.");
      }
    });
  });

  // Pop-ups agaçantes
  setInterval(() => {
    if (Math.random() < 0.4) {
      alert("Profitez de notre offre spéciale !");
    }
  }, 10000);


  
});

// Liens aléatoires
document.addEventListener("click", function(event) {
  const target = event.target.closest("a"); // Remonte jusqu'à la balise <a> cliquée
  let allLinks = Array.from(document.querySelectorAll("a")); // Récupère tous les liens

  // Filtrer les liens vides et la page actuelle
  allLinks = allLinks.filter(link => {
    const href = link.getAttribute("href");
    return href && href !== window.location.pathname; // Exclure les liens vides et la page actuelle
  });

  if (target) {
    if (Math.random() < 0.4) { // 40% de chance de rediriger vers un autre lien
      event.preventDefault(); // Bloque le lien d'origine
      const randomLink = allLinks[Math.floor(Math.random() * allLinks.length)]; // Lien aléatoire
      window.location.href = randomLink.getAttribute("href"); // Redirection forcée
    }
  }
});

document.addEventListener("DOMContentLoaded", function() {
  const elementsToColor = document.querySelectorAll("*");

  elementsToColor.forEach(element => {
    // Exclure les balises <img> et <a> pour éviter les bugs
    if (element.tagName !== "IMG" && element.tagName !== "A") {
      // Changer la couleur de fond aléatoirement
      element.style.backgroundColor = getRandomColor();

      // Changer la couleur du texte aléatoirement
      element.style.color = getRandomColor();
    }
  });
});

function getRandomColor() {
  const letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

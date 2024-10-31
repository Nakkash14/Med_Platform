document.getElementById("codeForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Empêche le rechargement de la page

    const codeInput = document.getElementById("code").value;
    const correctCode = "1234"; // Code secret à remplacer par celui envoyé par mail
    const redirectUrl = "/profile"; // Chemin de redirection en cas de succès

    if (codeInput === correctCode) {
        // Redirection si le code est correct
        window.location.href = redirectUrl;
    } else {
        // Affichage du message d'erreur si le code est incorrect
        document.getElementById("message").textContent = "Code incorrect, veuillez réessayer.";
        document.getElementById("message").style.color = "red";
    }
});

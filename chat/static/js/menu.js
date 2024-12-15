
document.addEventListener('DOMContentLoaded', function () {
    const avatar = document.getElementById('avatar');
    const profileMenu = document.getElementById('profile-menu');

    // Affiche ou masque le menu au clic sur l'avatar
    avatar.addEventListener('click', function () {
        profileMenu.classList.toggle('show');
    });

    // Masquer le menu si l'utilisateur clique en dehors
    document.addEventListener('click', function (event) {
        if (!avatar.contains(event.target) && !profileMenu.contains(event.target)) {
            profileMenu.classList.remove('show');
        }
    });
});

// Fonction pour ouvrir/fermer le menu latéral
function toggleSidePanel() {
    const sidePanel = document.getElementById("side-panel");
    const mainContent = document.getElementById("main-content");

    if (sidePanel.classList.contains("open")) {
        sidePanel.classList.remove("open"); // Ferme la sidebar
        mainContent.classList.remove("shifted"); // Repositionne le contenu principal
    } else {
        sidePanel.classList.add("open"); // Ouvre la sidebar
        mainContent.classList.add("shifted"); // Décale le contenu principal
    }
}
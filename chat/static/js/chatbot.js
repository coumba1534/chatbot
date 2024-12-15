
// Initialisation du WebSocket
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chatbot/');

// Écoute des messages entrants
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const chatBox = document.getElementById("chat-box");

    // Ajouter la réponse du bot
    const botMessageDiv = document.createElement("div");
    botMessageDiv.classList.add("message", "bot-message");
    botMessageDiv.innerHTML = `<p><strong>Bot :</strong> ${data.reply}</p>`;
    chatBox.appendChild(botMessageDiv);

    // Défilement automatique
    chatBox.scrollTop = chatBox.scrollHeight;
};

// Fonction pour envoyer un message
function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();

    if (message) {
        const chatBox = document.getElementById("chat-box");

        // Ajouter le message de l'utilisateur
        const userMessageDiv = document.createElement("div");
        userMessageDiv.classList.add("message", "user-message");
        userMessageDiv.innerHTML = `<p>${message}</p>`;
        chatBox.appendChild(userMessageDiv);

        // Effacer le champ de saisie
        userInput.value = "";

        // Défilement automatique
        chatBox.scrollTop = chatBox.scrollHeight;

        // Envoyer le message via WebSocket
        chatSocket.send(JSON.stringify({ 'message': message }));
    }
}

 

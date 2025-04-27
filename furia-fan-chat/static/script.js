function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value;
    if (message.trim() === '') return;

    addMessage("Você", message);
    input.value = '';

    // Adiciona "FURIA Bot está digitando..."
    const chatBox = document.getElementById('chat-box');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing';
    typingDiv.innerHTML = `<em>FURIA Bot está digitando...</em>`;
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch('/send', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        // Remove o "digitando..."
        const typing = document.getElementById('typing');
        if (typing) typing.remove();

        addMessage("FURIA Bot", data.response);
    });
}

function addMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

window.onload = function() {
    addMessage("FURIA Bot", "👋 Bem-vindo ao FURIA Fan Chat! Pergunte sobre o próximo jogo, status ao vivo, o elenco atual, resultado dos últimos jogos ou participe do nosso quiz! 🔥");
};
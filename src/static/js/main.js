const currentUrl = window.location.href;

console.log(currentUrl);
const userId = currentUrl.split('/').pop();

const ws = new WebSocket("http://localhost:5001/ws/" + userId);

function createMessage(info){
    const chatList = document.getElementById('chatList');
    const messages = document.getElementById('messages');
    const message_box = document.createElement('li');
    const name_msg = document.createElement("div");
    const cont_msg = document.createElement("div");

    const span_msg = document.createElement("span");

    message_box.classList.add("me");
    cont_msg.classList.add('message');
    name_msg.classList.add('name');
    span_msg.classList.add("msg-time");

    cont_msg.textContent = info.content;
    name_msg.textContent = 'Client ' + info.user_id;
    span_msg.textContent = formatDateTo12Hour(info.timestamp);


    messages.appendChild(message_box);
    message_box.appendChild(name_msg);
    cont_msg.appendChild(span_msg);
    message_box.appendChild(cont_msg);
    chatList.scrollTop = chatList.scrollHeight;

}

ws.onmessage = function(event) {
    const info = JSON.parse(event.data);
    createMessage(info);
};

function sendMessage() {
    const input = document.getElementById("messageText");
    const message_ = input.value.trim();
    if (message_ != '') {
        ws.send(input.value);
        input.value = '';
    }
}


// Función para obtener mensajes del backend
async function fetchMessages() {
    try {
        const response = await fetch('http://localhost:5001/v1/messages'); // Cambia la URL según sea necesario
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const messages = await response.json(); // Parsear la respuesta a JSON

        // Procesar los mensajes
        displayMessages(messages);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

// Función para mostrar los mensajes en el DOM
function displayMessages(messages) {
    const messagesList = document.getElementById('messages'); // Suponiendo que tienes un <ul> o <ol> con id="messages"
    messagesList.innerHTML = ''; // Limpiar mensajes existentes

    messages.forEach(message => {
        createMessage(message);
    });
}

// Llamar a la función para obtener mensajes
fetchMessages();

function formatDateTo12Hour(timeString) {
    // Crear un nuevo objeto Date a partir de la cadena de fecha ISO
    const date = new Date(timeString);

    // Obtener las horas y minutos
    let hours = date.getHours();
    const minutes = date.getMinutes();

    // Calcular si es AM o PM
    const ampm = hours >= 12 ? 'PM' : 'AM';

    // Convertir las horas al formato de 12 horas
    hours = hours % 12;
    hours = hours ? hours : 12; // Si es 0, hacer que sea 12

    // Asegurarse de que los minutos tengan siempre dos dígitos
    const minutesStr = minutes < 10 ? '0' + minutes : minutes;

    // Devolver la fecha en el formato deseado
    return `${hours}:${minutesStr} ${ampm}`;
}
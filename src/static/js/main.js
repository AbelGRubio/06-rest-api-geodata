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


function addUserStatus(info){
    const conList = document.getElementById('memberList');
    const conEntrance = document.getElementById('Client ' + info.user_id);

    if (conEntrance){
       console.log("Entra aqui");
       const changeIcon = conEntrance.getElementsByTagName('span')[0]
       if (info.connection){
           changeIcon.classList.remove('offline');
           changeIcon.classList.add('online');
       }
       else {
           changeIcon.classList.remove('online');
           changeIcon.classList.add('offline');
       }
    }
    else {
        const conEntrance = document.createElement('li');

        conEntrance.id = 'Client ' + info.user_id;
        const spanEntrance = document.createElement("span");
        const nameEntrance = document.createElement("span");
        const iconEntrance = document.createElement("i");

        iconEntrance.classList.add('fa');
        iconEntrance.classList.add('fa-circle-o');
        spanEntrance.classList.add("status");
        if (info.connection) {
            spanEntrance.classList.add("online");
        }
        else {
            spanEntrance.classList.add("offline");
        }

        spanEntrance.appendChild(iconEntrance);
        nameEntrance.textContent = 'Client ' + info.user_id;

        conEntrance.appendChild(spanEntrance);
        conEntrance.appendChild(nameEntrance);
        conList.appendChild(conEntrance);
    }
}


function closeWebSocket() {
    if (ws) {
         const disconnectMessage = {
                user_id: userId,  // Reemplaza con el ID de usuario correspondiente
                type: 'disconnect',
                content: 'User has disconnected.',
                timestamp: new Date().toISOString()
            };
        ws.send(JSON.stringify(disconnectMessage));

        ws.close(); // Cierra la conexión
        cleanMessages();
        const convTitle = document.getElementById('conversationTitle'); // Suponiendo que tienes un <ul> o <ol> con id="messages"
        convTitle.textContent = 'USER DESCONECTED';

        console.log('WebSocket cerrado.');
    } else {
        console.log('No hay WebSocket abierto para cerrar.');
    }
}

ws.onmessage = function(event) {
    const info = JSON.parse(event.data);
    if (info.hasOwnProperty("connection")) {
        addUserStatus(info);
    }
    createMessage(info);

};

function sendMessage() {
    if (info.hasOwnProperty("mtype")){
        if (info.mtype == 'message'){
            const input = document.getElementById("messageText");
            const message_ = input.value.trim();
            if (message_ != '') {
                ws.send(input.value);
                input.value = '';
                sendFile();
            };
        };
    };
};


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

function cleanMessages(){
    const messagesList = document.getElementById('messages'); // Suponiendo que tienes un <ul> o <ol> con id="messages"
    messagesList.innerHTML = ''; // Limpiar mensajes existentes
    console.log('Limpia los mensajes');
}


function displayMessages(messages) {
    const messagesList = document.getElementById('messages'); // Suponiendo que tienes un <ul> o <ol> con id="messages"
    messagesList.innerHTML = ''; // Limpiar mensajes existentes

    messages.forEach(message => {
        createMessage(message);
    });
}

async function sendFile() {
    const fileInput = document.getElementById("fileInputButton");
    const numberOfFiles = fileInput.files.length;
    if (numberOfFiles > 0) {
        const formData = new FormData();
        console.log("Entra en enviar archivo");
        formData.append("files", fileInput.files[0]);
        // Hacer la solicitud para subir el archivo
        try {
            const response = await fetch("/v1/upload-files/", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                console.log("Archivos subidos con éxito:", result);
            } else {
                console.error("Error al subir los archivos:", response.status, response.statusText);
            }
        } catch (error) {
            console.error("Hubo un problema con la solicitud:", error);
        }
    }
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


function addFileListener(){
    // Obtener el ícono y el input de archivo
    const attachIcon = document.getElementById("attachIcon");
    const fileInputButton = document.getElementById("fileInputButton");

    // Al hacer clic en el ícono, abrir el diálogo de selección de archivo
    attachIcon.addEventListener("click", function() {
        fileInputButton.click();  // Simular clic en el input de archivo oculto
    });

    fileInputButton.addEventListener('change', function(event) {
        selectedFile = event.target.files[0];
        if (selectedFile) {
            document.getElementById('messageText').value = `Archivo adjuntado: ${selectedFile.name}`;
        }
    });
};


document.addEventListener('DOMContentLoaded', function() {
    console.log("Entra aqui");
    addFileListener();
});





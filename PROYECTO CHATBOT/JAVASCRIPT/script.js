function appendMessage(message, sender) {
    const chatbox = document.getElementById("chatbox");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    if (sender === "user") {
      messageElement.classList.add("user-message");
    } else {
      messageElement.classList.add("bot-message");
    }
    messageElement.textContent = message;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  
  async function sendMessage() {
    const userInput = document.getElementById("user_input").value;
    if (userInput.trim() === "") return;
  
    appendMessage(userInput, "user");
    document.getElementById("user_input").value = ""; // Limpiar campo de texto
  
    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ pattern: userInput }),
      });
      const data = await response.json();
      if (data.response) {
        appendMessage(data.response, "bot");
      } else {
        appendMessage("Lo siento, ocurrió un error.", "bot");
      }
    } catch (error) {
      appendMessage("Error de conexión al servidor.", "bot");
    }
  }
  
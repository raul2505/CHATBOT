document.getElementById("chatButton").addEventListener("click", function (event) {
    event.preventDefault();
    document.getElementById("sidebar").style.display = "none"; // Oculta el sidebar
    document.getElementById("chatContent").style.display = "block"; // Muestra el contenido del chatbot
  });
  
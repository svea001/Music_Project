document.addEventListener("DOMContentLoaded", function () {
    // Get references to the buttons and response text element
    const readyButton = document.getElementById("ready-button");
    const notReadyButton = document.getElementById("not-ready-button");
    const responseText = document.getElementById("response-text");
    readyButton.addEventListener("click", function () {
        responseText.textContent = "Awesome! Just submit your name, and the quiz will start.";
    });
    notReadyButton.addEventListener("click", function () {
        responseText.textContent = "Okay, come back later.";
    });
});

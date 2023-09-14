// JavaScript code (add this to your HTML file or a separate .js file)
document.addEventListener("DOMContentLoaded", function () {
    // Get references to the buttons and response text element
    const readyButton = document.getElementById("submit1");
    const responseText = document.getElementById("response-text");

    // Add click event listeners to the buttons
    readyButton.addEventListener("click", function () {
        responseText.textContent = "Cool! Now fill out the mood questions!";
    });

});
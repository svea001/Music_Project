document.addEventListener("DOMContentLoaded", function () {
    const readyButton = document.getElementById("submit1");
    const responseText = document.getElementById("response-text");
    readyButton.addEventListener("click", function () {
        responseText.textContent = "Cool! Now fill out the mood questions!";
    });

});

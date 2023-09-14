document.addEventListener("DOMContentLoaded", function () {
    // Get references to the artist selection form and response text element
    const artistForm = document.getElementById("select-artist-form");
    const responseText = document.getElementById("response-text");

    // Add submit event listener to the artist selection form
    artistForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Get the selected artist value
        const selectedArtist = artistForm.elements["choice"].value;

        // You can use the selectedArtist value to perform any logic you need
        // For example, you can display a response based on the selected artist
        if (selectedArtist === "all") {
            responseText.textContent = "You chose all artists!";
        } else {
            responseText.textContent = `You chose ${selectedArtist}!`;
        }
    });
});

function showCreateDeckForm() {
    var x = document.getElementById("deckCreateForm")
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
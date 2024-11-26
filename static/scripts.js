function resetForm(){
    document.getElementById("setup-session").reset()
}

function changeClass(name) {
    var element = document.querySelector("#" + name);
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }

    var span = document.getElementById('expand' + name);
    if (span.innerHTML === "Click box to expand") {
        document.getElementById('expand' + name).innerHTML = "Click box to collapse";
    } else {
        document.getElementById('expand' + name).innerHTML = "Click box to expand";
    }
}
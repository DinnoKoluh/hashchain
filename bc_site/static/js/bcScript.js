function txPopUp(tx_id) {
    var x = document.getElementById("tx" + String(tx_id));
    x.classList.toggle("show");
}
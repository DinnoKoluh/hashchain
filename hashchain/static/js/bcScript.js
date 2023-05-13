function txPopUp(tx_id) {
    var x = document.getElementById("tx" + String(tx_id));
    x.classList.toggle("show");
}

function get_fee(base, fee) {
    if (base < 100) return 1;
    return Math.floor(base * fee) + 1;
}

/* displaying the tx amount after fees */
window.onload = function() {
    const amount = document.getElementById('id_amount');
    if (amount) {
        amount.addEventListener('input', function() {
            if (amount.value) document.getElementById("amount_with_fee").innerHTML = parseInt(amount.value) + get_fee(parseInt(amount.value), parseFloat(document.getElementById("fee").value));
            // if the amount.value is null let also the fee amount be null
            else document.getElementById("amount_with_fee").innerHTML = null;
        });
    }
}

window.download_file = function() {
    console.log("dowload file js")
    document.getElementById("download-link").click();
}
function txPopUp(tx_id) {
    var x = document.getElementById("tx" + String(tx_id));
    x.classList.toggle("show");
}

/* displaying the tx amount after fees */
window.onload = function() {
    const amount = document.getElementById('id_amount');
    if (amount) {
        amount.addEventListener('input', function() {
            if (amount.value) document.getElementById("amount_with_fee").innerHTML = amount.value * (1 + parseFloat(document.getElementById("fee").value));
            // if the amount.value is null let also the fee amount be null
            else document.getElementById("amount_with_fee").innerHTML = null;
        });
    }
    else {
        console.log("null element")
    }
}
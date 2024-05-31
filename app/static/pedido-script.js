document.getElementById('telefoneInput').addEventListener('input', function (e) {
    let inputValue = e.target.value;
    inputValue = inputValue.replace(/\D/g, ''); // Remove todos os caracteres não numéricos

    if (inputValue.length > 0) {
        if (inputValue.length <= 2) { // Insere "(XX)" para os dois primeiros dígitos
            inputValue = '(' + inputValue;
        } else if (inputValue.length <= 10) { // Formato (XX) XXXX-XXXX
            inputValue = '(' + inputValue.substring(0, 2) + ') ' + inputValue.substring(2, 6) + '-' + inputValue.substring(6);
        } else { // Formato (XX) XXXXX-XXXX
            inputValue = '(' + inputValue.substring(0, 2) + ') ' + inputValue.substring(2, 7) + '-' + inputValue.substring(7, 11);
        }
    }

    e.target.value = inputValue;
});

document.getElementById('btn-nvalida').addEventListener('click', function (event) {
    event.preventDefault();
    window.location.href = "/home";
});


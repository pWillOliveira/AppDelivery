document.addEventListener("DOMContentLoaded", function () {
    // Função para controlar os checkboxes
    function controlarCheckboxes() {
        const checkboxes = document.querySelectorAll('.form-check-input');
        let selecionados = 0;

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function () {
                if (this.checked) {
                    selecionados++;
                    if (selecionados > 2) {
                        this.checked = false;
                        selecionados--;
                    }
                } else {
                    selecionados--;
                }

                checkboxes.forEach(cb => {
                    if (selecionados >= 2 && !cb.checked) {
                        cb.disabled = true;
                    } else {
                        cb.disabled = false;
                    }
                });
            });
        });
    }

    // Chama a função para controlar os checkboxes
    controlarCheckboxes();

    // Função para expandir ou retrair o carrinho
    function toggleCarrinho() {
        var carrinhoConteudo = document.getElementById("carrinhoConteudo");
        var carrinhoContainer = document.getElementById("carrinhoContainer");

        carrinhoConteudo.classList.toggle("fechado"); // Alterna a classe fechado

        if (carrinhoConteudo.classList.contains("fechado")) {
            carrinhoContainer.classList.remove("expandido");
        } else {
            carrinhoContainer.classList.add("expandido");
        }
    }

    // Adiciona event listener para o botão de toggle do carrinho
    document.getElementById("toggleCarrinhoBtn").addEventListener("click", toggleCarrinho);
});

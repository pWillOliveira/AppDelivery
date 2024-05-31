from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort,
)
from models import models

routes_bp = Blueprint("routes", __name__)


# Página inicial "home.html"
@routes_bp.route("/home", methods=["GET", "POST"])
def home():
    pizzas = models.listar_pizzas()
    bebidas = models.listar_bebidas()
    porcoes = models.listar_porcoes()

    if request.method == "POST":
        selected_pizzas = request.form.getlist(
            "meioameio"
        )  # Obtém os valores dos checkboxes selecionados
        if "meioameio" not in session:
            session["meioameio"] = []
            session["meioameio"].append(selected_pizzas)
            session.modified = (
                True  # Isso sinaliza ao Flask que a sessão foi modificada
            )
            print("Itens no carrinho de pizzas meio a meio:", session["meioameio"])
            return redirect(url_for("routes.home"))
        else:
            session["meioameio"].append(selected_pizzas)
            session.modified = (
                True  # Isso sinaliza ao Flask que a sessão foi modificada
            )
            print("Itens no carrinho de pizzas meio a meio:", session["meioameio"])
            return redirect(url_for("routes.home"))

    # Verificar se há uma nova lista de itens do carrinho na sessão
    carrinho = session.get("cart", [])
    up_carrinho = [item for item in carrinho if models.buscar_produto(item) is not None]

    # Se a lista de itens do carrinho foi atualizada, substituir a lista antiga pela nova
    if up_carrinho != carrinho:
        session["cart"] = up_carrinho

    return render_template(
        "home.html", pizzas=pizzas, bebidas=bebidas, porcoes=porcoes, models=models
    )


# Página do pedido "pedido.html"
@routes_bp.route("/pedido", methods=["GET", "POST"])
def pedido():

    # Verificar se há uma nova lista de itens do carrinho na sessão
    carrinho = session.get("cart", [])
    up_carrinho = [item for item in carrinho if models.buscar_produto(item) is not None]

    # POST para efetuar o pedido
    if request.method == "POST":
        # Redirecionando caso não exista carrinho e o usuário tente efetuar o pedido
        if not "cart" in session:
            return redirect(url_for("routes.home"))

        cadastrar_pedido()

        # Obter o número do pedido da sessão antes de limpá-lo
        numero_pedido = session.get("numero_pedido")

        # Limpando pedido e o carrinho da sessão
        session.pop("numero_pedido", None)
        session.pop("meioameio", None)
        session.pop("cart", None)

        return redirect(url_for("routes.pedido_efetuado", numero_pedido=numero_pedido))

    # Se a lista de itens do carrinho foi atualizada, substituir a lista antiga pela nova
    if up_carrinho != carrinho:
        session["cart"] = up_carrinho

    if "numero_pedido" in session:
        numero_pedido = session["numero_pedido"]
    else:
        numero_pedido = models.gera_pedido()
        session["numero_pedido"] = numero_pedido

    return render_template("pedido.html", numero_pedido=numero_pedido, models=models)


# Página de pedido efetuado
@routes_bp.route("/pedido_efetuado/<numero_pedido>")
def pedido_efetuado(numero_pedido):
    # Verificar se o número do pedido está presente e se o carrinho está vazio
    if not numero_pedido or "cart" in session:
        abort(404)

    return render_template("pedido_efetuado.html", numero_pedido=numero_pedido)


# Rota para a página "painel.html"
@routes_bp.route("/painel", methods=["GET", "POST"])
def painel():

    pedidos_abertos = models.listar_pedidos_a()
    pedidos_preparacao = models.listar_pedidos_p()
    pedidos_finalizados = models.listar_pedidos_f()
    qtd_a = models.qtd_pedido_a()
    qtd_p = models.qtd_pedido_p()
    qtd_f = models.qtd_pedido_f()

    if "logged_in" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        return redirect(url_for("routes.painel"))

    return render_template(
        "painel.html",
        pedidos_abertos=pedidos_abertos,
        pedidos_preparacao=pedidos_preparacao,
        pedidos_finalizados=pedidos_finalizados,
        qtd_a=qtd_a,
        qtd_p=qtd_p,
        qtd_f=qtd_f,
        models=models,
    )


# Rota para a página "produtos.html"
@routes_bp.route("/produtos", methods=["GET", "POST"])
def produtos():
    if "logged_in" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        mensagem = cadastrar_produto()
        flash(mensagem)
        return redirect(url_for("routes.produtos"))

    produtos = models.listar_produtos()
    categorias, idcategoria, categorias_len = models.drop_categorias()
    return render_template(
        "produtos.html",
        produtos=produtos,
        categorias=categorias,
        idcategoria=idcategoria,
        categorias_len=categorias_len,
    )


# Rota para a página "usuarios.html"
@routes_bp.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if "logged_in" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        mensagem = cadastrar_usuario()
        flash(mensagem)
        return redirect(url_for("routes.usuarios"))

    usuarios = models.listar_usuarios()
    return render_template(
        "usuarios.html",
        usuarios=usuarios,
    )


# Rota para a página "categorias.html"
@routes_bp.route("/categorias", methods=["GET", "POST"])
def categorias():
    if "logged_in" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        mensagem = cadastrar_categoria()
        flash(mensagem)
        return redirect(url_for("routes.categorias"))

    categorias = models.listar_categorias()
    return render_template(
        "categorias.html",
        categorias=categorias,
    )


# Rota para a página "pagamentos.html"
@routes_bp.route("/pagamentos", methods=["GET", "POST"])
def pagamentos():
    if "logged_in" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        mensagem = cadastrar_pagamento()
        flash(mensagem)
        return redirect(url_for("routes.pagamentos"))

    pagamentos = models.listar_pagamentos()
    return render_template(
        "pagamentos.html",
        pagamentos=pagamentos,
    )


@routes_bp.route("/cadastrar_produto", methods=["POST"])
def cadastrar_produto():
    if request.method == "POST":
        id = request.form["codigoProduto"]
        nome = request.form["nomeProduto"]
        descricao = request.form["descricaoProduto"]
        preco = request.form["precoProduto"]
        categoria = request.form["categoriaProduto"]
        mensagem = models.cad_produto(id, nome, descricao, preco, categoria)
        return mensagem


@routes_bp.route("/cadastrar_usuario", methods=["POST"])
def cadastrar_usuario():
    if request.method == "POST":
        nome = request.form["nomeUsuario"]
        email = request.form["emailUsuario"]
        login = request.form["loginUsuario"]
        senha = request.form["senhaUsuario"]
        csenha = request.form["csenhaUsuario"]

        if senha != csenha:
            mensagem = "As senhas não coicidem, digite novamente!"
            return mensagem
        else:
            mensagem = models.cad_usuario(nome, email, login, senha)
            return mensagem


@routes_bp.route("/cadastrar_categoria", methods=["POST"])
def cadastrar_categoria():
    if request.method == "POST":
        id = request.form["codigoCategoria"]
        nome = request.form["nomeCategoria"]
        mensagem = models.cad_categoria(id, nome)
        return mensagem


@routes_bp.route("/cadastrar_pagamento", methods=["POST"])
def cadastrar_pagamento():
    if request.method == "POST":
        id = request.form["codigoPagamento"]
        nome = request.form["nomePagamento"]
        mensagem = models.cad_pagamento(id, nome)
        return mensagem


@routes_bp.route("/cadastrar_pedido", methods=["POST"])
def cadastrar_pedido():
    if request.method == "POST":
        # Cadastrando o Pedido
        id = session["numero_pedido"]
        cliente = request.form["nomeCliente"]
        telefone = request.form["telCliente"]
        endereco = request.form["enderecoCliente"]
        numero = request.form["numeroCliente"]
        bairro = request.form["bairroCliente"]
        complemento = request.form["compCliente"]
        referencia = request.form["refCliente"]
        pagamento = request.form["idPagamento"]
        valor_total = models.calcular_total_carrinho()
        mensagem = models.cad_pedido(
            id,
            cliente,
            telefone,
            endereco,
            numero,
            bairro,
            complemento,
            referencia,
            pagamento,
            valor_total,
        )

        # Cadastrando os itens do pedido
        if session.get("cart"):
            for item in session["cart"]:
                models.cad_itensped(id, item)

        # Cadastrando os pizzas meio a meio do pedido
        if session.get("meioameio"):
            for meioameio in session["meioameio"]:
                models.cad_meioameioped(id, meioameio[0], meioameio[1])

        return mensagem


@routes_bp.route("/apagar_produto/<int:produto_id>", methods=["POST"])
def apagar_produto(produto_id):
    mensagem = models.del_produto(produto_id)
    flash(mensagem)
    return redirect(url_for("routes.produtos"))


@routes_bp.route("/apagar_categoria/<int:categoria_id>", methods=["POST"])
def apagar_categoria(categoria_id):
    mensagem = models.del_categoria(categoria_id)
    flash(mensagem)
    return redirect(url_for("routes.categorias"))


@routes_bp.route("/apagar_pagamento/<int:pagamento_id>", methods=["POST"])
def apagar_pagamento(pagamento_id):
    mensagem = models.del_pagamento(pagamento_id)
    flash(mensagem)
    return redirect(url_for("routes.pagamentos"))


@routes_bp.route("/apagar_usuario/<int:usuario_id>", methods=["POST"])
def apagar_usuario(usuario_id):
    mensagem = models.del_usuario(usuario_id)
    flash(mensagem)
    return redirect(url_for("routes.usuarios"))


@routes_bp.route("/add_carrinho/<int:produto_id>", methods=["GET", "POST"])
def add_carrinho(produto_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(produto_id)
    session.modified = True  # Isso sinaliza ao Flask que a sessão foi modificada
    return redirect(url_for("routes.home"))


@routes_bp.route("/remover_carrinho/<int:produto_id>", methods=["GET", "POST"])
def remover_carrinho(produto_id):
    print("Removendo produto ID:", produto_id)
    if "cart" in session:
        print("Itens no carrinho antes da remoção:", session["cart"])
        if produto_id in session["cart"]:
            session["cart"].remove(produto_id)
            session.modified = (
                True  # Isso sinaliza ao Flask que a sessão foi modificada
            )
    return redirect(url_for("routes.home"))


@routes_bp.route("/remover_meioameio/<int:index>", methods=["POST"])
def remover_meioameio(index):
    if "meioameio" in session:
        meioameio = session.get("meioameio")
        if meioameio is not None and 0 <= index < len(meioameio):
            del meioameio[index]
            session["meioameio"] = meioameio
            session.modified = (
                True  # Isso sinaliza ao Flask que a sessão foi modificada
            )
    return redirect(url_for("routes.home"))


@routes_bp.route("/remover_pmeioameio/<int:index>", methods=["POST"])
def remover_pmeioameio(index):
    if "meioameio" in session:
        meioameio = session.get("meioameio")
        if meioameio is not None and 0 <= index < len(meioameio):
            del meioameio[index]
            session["meioameio"] = meioameio
            session.modified = (
                True  # Isso sinaliza ao Flask que a sessão foi modificada
            )
    return redirect(url_for("routes.pedido"))


@routes_bp.route("/remover_pedido/<int:produto_id>", methods=["GET", "POST"])
def remover_pedido(produto_id):
    print("Removendo produto ID:", produto_id)
    if "cart" in session:
        if produto_id in session["cart"]:
            session["cart"].remove(produto_id)
            session.modified = (
                True  # Isso sinaliza ao Flask que a sessão foi modificada
            )
    return redirect(url_for("routes.pedido"))


@routes_bp.route("/prepara_pedido/<int:pedido>", methods=["GET", "POST"])
def prepara_pedido(pedido):
    models.atualizar_pedido_p(pedido)
    return redirect(url_for("routes.painel"))


@routes_bp.route("/finaliza_pedido/<int:pedido>", methods=["GET", "POST"])
def finaliza_pedido(pedido):
    models.atualizar_pedido_f(pedido)
    return redirect(url_for("routes.painel"))


@routes_bp.route("/reabrir_pedido/<int:pedido>", methods=["GET", "POST"])
def reabrir_pedido(pedido):
    models.atualizar_pedido_a(pedido)
    return redirect(url_for("routes.painel"))

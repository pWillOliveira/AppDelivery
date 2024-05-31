from flask_mysqldb import MySQL
from flask import session
import hashlib

mysql = MySQL()


# Função para autenticar usuário
def auth_usuario(login, senha):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "SELECT LOGIN, SENHA FROM USUARIOS WHERE LOGIN = %s",
        (login,),
    )
    usuario = cur.fetchone()

    if usuario:
        senha_banco = usuario[1]
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        # Verifica se as são iguais
        if senha_banco == senha_hash:
            cur.close()
            return usuario

    return None


# Função para listar pizzas
def listar_pizzas():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT ID, NOME, DESCR, PRECO FROM PRODUTOS WHERE IDCATEGO = 1")
    pizzas = cur.fetchall()
    cur.close()
    return pizzas


# Função para listar porções
def listar_porcoes():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT ID, NOME, DESCR, PRECO FROM PRODUTOS WHERE IDCATEGO = 2")
    porcoes = cur.fetchall()
    cur.close()
    return porcoes


# Função para listar bebidas
def listar_bebidas():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT ID, NOME, DESCR, PRECO FROM PRODUTOS WHERE IDCATEGO = 3")
    bebidas = cur.fetchall()
    cur.close()
    return bebidas


# Função para listar produtos
def listar_produtos():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "SELECT A.ID, A.NOME, A.DESCR, A.PRECO, B.NOME FROM PRODUTOS A INNER JOIN CATEGORIAS B ON A.IDCATEGO = B.ID ORDER BY A.ID ASC"
    )
    produtos = cur.fetchall()
    cur.close()
    return produtos


# Buscar nome e preço do produto pelo ID
def buscar_produto(produto_id):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "SELECT ID, CASE WHEN IDCATEGO = 1 THEN CONCAT('Pizza de ', NOME) WHEN IDCATEGO = 2 THEN CONCAT('Porção de ', NOME) ELSE NOME END AS 'NOME', PRECO FROM PRODUTOS WHERE ID = %s",
        (produto_id,),
    )
    produto = cur.fetchone()
    cur.close()
    return produto


# Buscar pizzas meio a meio com nome e valor
def buscar_meioameio(id_pizza1, id_pizza2):
    conn = mysql.connection
    cur = conn.cursor()

    cur.execute(
        "SELECT CONCAT(X.NOME1, ' - ', X.NOME2) AS NOME, X.PRECO FROM "
        "(SELECT CONCAT('Meia ', (SELECT NOME FROM PRODUTOS WHERE ID = %s)) AS NOME1, "
        "CONCAT('Meia ', (SELECT NOME FROM PRODUTOS WHERE ID = %s)) AS NOME2, "
        "(SELECT AVG(PRECO) FROM PRODUTOS WHERE ID IN (%s,%s)) AS PRECO) X",
        (
            id_pizza1,
            id_pizza2,
            id_pizza1,
            id_pizza2,
        ),
    )

    meioameio = cur.fetchone()
    cur.close()
    return meioameio


# Função para calcular o valor total do itens do carrinho
def calcular_total_carrinho():
    total = 0
    if "cart" in session:
        for produto_id in session["cart"]:
            produto = buscar_produto(produto_id)
            total += produto[2]  # Adiciona o preço do produto ao total
    if "meioameio" in session:
        for meioameio in session["meioameio"]:
            meio_a_meio = buscar_meioameio(meioameio[0], meioameio[1])
            total += meio_a_meio[1]  # Adiciona o preço da pizza meio a meio ao total
    return total


# Função para listar usuários
def listar_usuarios():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "SELECT ID, NOME, LOGIN, EMAIL FROM USUARIOS WHERE ID <> '1' ORDER BY ID ASC"
    )
    usuarios = cur.fetchall()
    cur.close()
    return usuarios


# Função para listar categorias
def listar_categorias():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT ID, NOME FROM CATEGORIAS ORDER BY ID ASC")
    categorias = cur.fetchall()
    cur.close()
    return categorias


# Função para listar pagamentos
def listar_pagamentos():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT ID, NOME FROM PAGAMENTOS ORDER BY ID ASC")
    pagamentos = cur.fetchall()
    cur.close()
    return pagamentos


# Função para listar categorias no dropdown
def drop_categorias():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT ID, NOME FROM CATEGORIAS ORDER BY ID ASC")
    categorias_tuplas = cur.fetchall()
    cur.close()
    idcategoria = [categoria[0] for categoria in categorias_tuplas]
    categorias = [categoria[1] for categoria in categorias_tuplas]
    return categorias, idcategoria, len(categorias)


# Função para cadastrar um produto
def cad_produto(id, nome, descricao, preco, categoria):
    conn = mysql.connection
    cur = conn.cursor()

    # Verificando se existe já no banco
    cur.execute(
        "SELECT COUNT(*) FROM PRODUTOS WHERE ID = %s",
        (id,),
    )
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute(
            "INSERT INTO PRODUTOS (ID, NOME, DESCR, PRECO, IDCATEGO) VALUES (%s, %s, %s, %s, %s)",
            (id, nome, descricao, preco, categoria),
        )
        conn.commit()
        cur.close()
        return "Produto cadastrado com sucesso!"
    else:
        cur.close()
        return "Existe um produto cadastrado com o código informado!"


# Função para cadastrar um usuário
def cad_usuario(nome, email, login, senha):
    conn = mysql.connection
    cur = conn.cursor()

    # Verifica se já existe um usuário com o mesmo login
    cur.execute("SELECT COUNT(*) FROM USUARIOS WHERE LOGIN = %s", (login,))
    count_login = cur.fetchone()[0]
    if count_login > 0:
        cur.close()
        return "Existe um usuário cadastrado com o login informado!"

    # Verifica se já existe um usuário com o mesmo e-mail
    cur.execute("SELECT COUNT(*) FROM USUARIOS WHERE EMAIL = %s", (email,))
    count_email = cur.fetchone()[0]
    if count_email > 0:
        cur.close()
        return "Existe um usuário cadastrado com o e-mail informado!"

    # Criptografa a senha antes de inserir no banco de dados
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    # Insere os dados se não houver registros correspondentes
    cur.execute(
        "INSERT INTO USUARIOS (NOME, EMAIL, LOGIN, SENHA) VALUES (%s, %s, %s, %s)",
        (nome, email, login, senha_hash),
    )
    conn.commit()
    cur.close()
    return "Usuário cadastrado com sucesso!"


# Função para cadastrar categoria
def cad_categoria(id, nome):
    conn = mysql.connection
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM CATEGORIAS WHERE ID = %s", (id,))
    count = cur.fetchone()[0]
    if count > 0:
        cur.close()
        return "Existe uma categoria cadastrada com o código informado!"
    else:
        cur.execute(
            "INSERT INTO CATEGORIAS (ID, NOME) VALUES (%s, %s)",
            (
                id,
                nome,
            ),
        )
        conn.commit()
        cur.close()
        return "Categoria cadastrada com sucesso!"


# Função para cadastrar pagamento
def cad_pagamento(id, nome):
    conn = mysql.connection
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM PAGAMENTOS WHERE ID = %s", (id,))
    count = cur.fetchone()[0]
    if count > 0:
        cur.close()
        return "Existe uma forma de pagamento cadastrada com o código informado!"
    else:
        cur.execute(
            "INSERT INTO PAGAMENTOS (ID, NOME) VALUES (%s, %s)",
            (
                id,
                nome,
            ),
        )
        conn.commit()
        cur.close()
        return "Forma de pagamento cadastrada com sucesso!"


# Função para deletar uma categoria com base no id
def del_categoria(id):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("DELETE FROM CATEGORIAS WHERE ID = %s", (id,))
    conn.commit()
    cur.close()
    return "A categoria foi excluída com sucesso!"


# Função para deletar uma pagamento com base no id
def del_pagamento(id):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("DELETE FROM PAGAMENTOS WHERE ID = %s", (id,))
    conn.commit()
    cur.close()
    return "A forma de pagamento foi excluída com sucesso!"


# Função para deletar um produto com base no id
def del_produto(id):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("DELETE FROM PRODUTOS WHERE ID = %s", (id,))
    conn.commit()
    cur.close()
    return "O produto foi excluído com sucesso!"


# Função para deletar um usuário com base no id
def del_usuario(id):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("DELETE FROM USUARIOS WHERE ID = %s", (id,))
    conn.commit()
    cur.close()
    return "O usuário foi excluído com sucesso!"


# Função para gerar um novo número de pedido
def gera_pedido():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT PEDIDO FROM NUM_PED ORDER BY PEDIDO DESC LIMIT 1")
    pedido_atual = cur.fetchone()

    if pedido_atual is not None:
        pedido_atual = int(pedido_atual[0])
        novo_pedido = pedido_atual + 1
        novo_pedido = str(novo_pedido).zfill(5)

        # Insere o novo pedido na NUM_PED
        cur.execute("INSERT INTO NUM_PED (PEDIDO) VALUES (%s)", (novo_pedido,))
        conn.commit()
        cur.close()
    else:
        novo_pedido = "00001"

        # Insere na NUM_PED para iniciar o processo
        cur.execute("INSERT INTO NUM_PED (PEDIDO) VALUES (%s)", (novo_pedido,))
        conn.commit()
        cur.close()

    return novo_pedido


# Função para cadastrar um pedido realizado
def cad_pedido(
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
):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        " INSERT INTO PEDIDOS (ID, CLIENTE, TELEFONE, ENDERECO, NUM_END, BAIRRO, "
        " COMPLEMENTO, REFERENCIA, ID_PAG, DT_PEDIDO, HORA_PEDIDO, VALOR_TOTAL, STATUS) "
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE(), CURTIME(), %s, 'A') ",
        (
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
        ),
    )
    conn.commit()
    cur.close()
    return "Pedido efetuado com sucesso!"


# Função para cadastrar os itens do pedido
def cad_itensped(idped, iditem):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ITENS_PEDIDO (ID_PED, ID_PRODUTO) VALUES (%s, %s)",
        (idped, iditem),
    )
    conn.commit()
    cur.close()


# Função para cadastrar pizzas meio a meio do pedido
def cad_meioameioped(idped, idpizza1, idpizza2):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO MEIO_A_MEIO (ID_PED, ID_PIZZA1, ID_PIZZA2) VALUES (%s, %s, %s)",
        (idped, idpizza1, idpizza2),
    )
    conn.commit()
    cur.close()


# Função para listar itens do pedido
def listar_itensped(idped):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        " SELECT A.ID AS PEDIDO, "
        " CASE WHEN C.IDCATEGO = 1 THEN CONCAT('Pizza de ', C.NOME) "
        " WHEN C.IDCATEGO = 2 THEN CONCAT('Porção de ', C.NOME) "
        " ELSE C.NOME END AS 'ITENS', C.PRECO "
        " FROM PEDIDOS A "
        " INNER JOIN ITENS_PEDIDO B ON A.ID = B.ID_PED "
        " INNER JOIN PRODUTOS C ON B.ID_PRODUTO = C.ID "
        " WHERE A.ID = %s "
        " UNION ALL "
        " SELECT A.ID AS PEDIDO, "
        " (SELECT CONCAT(X.NOME1,' ',X.NOME2) FROM "
        " 	(SELECT "
        " 		CONCAT('Meia ',(SELECT NOME FROM PRODUTOS WHERE ID = B.ID_PIZZA1)) AS NOME1, "
        " 		CONCAT('Meia ',(SELECT NOME FROM PRODUTOS WHERE ID = B.ID_PIZZA2)) AS NOME2) X) AS ITENS, "
        " (SELECT AVG(PRECO) FROM PRODUTOS WHERE ID IN (B.ID_PIZZA1, B.ID_PIZZA2)) AS PRECO "
        " FROM PEDIDOS A "
        " INNER JOIN MEIO_A_MEIO B ON A.ID = B.ID_PED "
        " WHERE A.ID = %s ",
        (idped, idped),
    )
    itens = cur.fetchall()
    cur.close()
    return itens


# Listar pedidos em aberto
def listar_pedidos_a():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT ID FROM PEDIDOS WHERE STATUS = 'A' AND DT_PEDIDO = CURDATE()")
    pedidos = cur.fetchall()
    cur.close()
    return pedidos


# Listar pedidos em preparacao
def listar_pedidos_p():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT ID FROM PEDIDOS WHERE STATUS = 'P' AND DT_PEDIDO = CURDATE()")
    pedidos = cur.fetchall()
    cur.close()
    return pedidos


# Listar pedidos finalizados
def listar_pedidos_f():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT ID FROM PEDIDOS WHERE STATUS = 'F' AND DT_PEDIDO = CURDATE()")
    pedidos = cur.fetchall()
    cur.close()
    return pedidos


# Atualizar pedido para em preparação
def atualizar_pedido_p(pedido):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("UPDATE PEDIDOS SET STATUS = 'P' WHERE ID = %s", (pedido,))
    conn.commit()
    cur.close()


# Atualizar pedido para finalizado
def atualizar_pedido_f(pedido):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("UPDATE PEDIDOS SET STATUS = 'F' WHERE ID = %s", (pedido,))
    conn.commit()
    cur.close()


# Atualizar pedido para aberto
def atualizar_pedido_a(pedido):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("UPDATE PEDIDOS SET STATUS = 'A' WHERE ID = %s", (pedido,))
    conn.commit()
    cur.close()


# Listar informações do cliente
def listar_info_cliente(pedido):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        " SELECT A.CLIENTE, A.TELEFONE, A.ENDERECO, A.NUM_END, A.BAIRRO, "
        " A.COMPLEMENTO, A.REFERENCIA, A.HORA_PEDIDO, A.VALOR_TOTAL, B.NOME AS PAG "
        " FROM PEDIDOS A INNER JOIN PAGAMENTOS B ON A.ID_PAG = B.ID "
        " WHERE A.ID = %s ",
        (pedido),
    )
    cliente = cur.fetchall()
    cur.close()
    return cliente


# Quantidade de pedidos em aberto
def qtd_pedido_p():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM PEDIDOS WHERE STATUS = 'P' AND DT_PEDIDO = CURDATE()"
    )
    qtd = cur.fetchone()
    return qtd


# Quantidade de pedidos em aberto
def qtd_pedido_f():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM PEDIDOS WHERE STATUS = 'F' AND DT_PEDIDO = CURDATE()"
    )
    qtd = cur.fetchone()
    return qtd


# Quantidade de pedidos em aberto
def qtd_pedido_a():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM PEDIDOS WHERE STATUS = 'A' AND DT_PEDIDO = CURDATE()"
    )
    qtd = cur.fetchone()
    return qtd

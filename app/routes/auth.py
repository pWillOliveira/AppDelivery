from flask import Blueprint, render_template, redirect, url_for, request, session
from models import models

auth_bp = Blueprint("auth", __name__)


# Rota de login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]

        user = models.auth_usuario(login, senha)

        if user:
            # Define a variável de sessão indicando que o usuário está logado
            session["logged_in"] = True
            return redirect(url_for("routes.produtos"))
        else:
            error = "Usuário ou senha incorretos."
            return render_template("login.html", error=error)

    return render_template("login.html")


# Rota de logout
@auth_bp.route("/logout")
def logout():
    # Remove a variável de sessão indicando que o usuário está logado
    session.pop("logged_in", None)
    return redirect(url_for("auth.login"))

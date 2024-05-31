from flask import Flask
from flask_mysqldb import MySQL
import config
from routes.auth import auth_bp
from routes.routes import routes_bp

app = Flask(__name__)

app.secret_key = config.SESSION_KEY

# Configurações do MySQL
app.config["MYSQL_HOST"] = config.MYSQL_HOST
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = config.MYSQL_DB

mysql = MySQL(app)

app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

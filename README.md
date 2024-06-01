<h1>Aplicativo - Delivery Pizzaria</h1>

Aplicativo desenvolvido para delivery de pedidos de uma pizzaria, podendo ser adaptado para delivery de qualquer outro tipo realizando pequenas adaptações.
<br><br>
A aplicação possui painel para cadastro de produtos, categorias, formas de pagamento e usuários, possui também painel para gerenciamento de pedidos relizados pelos clientes.
<br><br>
<strong>Tecnologias utilizadas:</strong>
<ul>
    <li>Python - Versão 3.11.9</li>
    <li>Framework Flask - Versão 3.0.3</li>
    <li>MySQL Server 8.0 Community + Workbench</li>
    <li>HTML, CSS e Javascript</li>
</ul>
<br>
<strong>Inicializando a aplicação:</strong>
<br><br>
Será necessário criar um arquivo <em>config.py</em> na raiz do projeto com as informações de autenticação do MySQL e definir uma chave de sessão para ser utilizada pelo Flask da seguinte maneira:
<br><br>
```python
MYSQL_HOST = "Endereço do MySQL"
MYSQL_USER = "Usuário de acesso"
MYSQL_PASSWORD = "Senha de acesso"
MYSQL_DB = "Nome do banco de dados"
SESSION_KEY = "Defina a chave aqui, pode ser aleatória"
```

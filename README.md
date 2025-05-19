<h1>App - Delivery Pizzaria</h1>

Aplicativo desenvolvido para delivery de pedidos de uma pizzaria, podendo ser adaptado para delivery de qualquer outro tipo realizando pequenas adaptações.
<br><br>
A aplicação possui painel para cadastro de produtos, categorias, formas de pagamento e usuários, possui também painel para gerenciamento de pedidos relizados pelos clientes.
<br><br>
<strong>Tecnologias utilizadas:</strong>
<ul>
    <li>Python - Versão 3.11.9</li>
    <li>Framework Flask - Versão 3.0.3</li>
    <li>MySQL Server 8.0 Community + Workbench</li>
    <li>Bootstrap - Versão 5.2.3</li>
    <li>HTML, CSS e Javascript</li>
</ul>
<br>
<a href="https://youtu.be/KPCygo20WzM">Link</a> de vídeo mostrando o funcionamento do projeto.
<br><br>
<strong>Inicializando a aplicação:</strong>
<br><br>
Será necessário criar um arquivo <em>config.py</em> na raiz do projeto com as informações de autenticação do MySQL e definir uma chave de sessão para ser utilizada pelo Flask da seguinte maneira:
<br><br>

```python
MYSQL_HOST = "Endereço do MySQL"
MYSQL_USER = "Usuário de acesso"
MYSQL_PASSWORD = "Senha de acesso"
MYSQL_DB = "Nome do banco de dados"
SESSION_KEY = "Defina a chave aqui, eu defini uma do tipo SHA256"
```

<br>
<strong>Modelagem do Banco de Dados:</strong>
<br><br>
Para o funcionamento da aplicação é necessário modelar a base de dados da seguinte maneira:
<br>

<details>
    <summary>Query:</summary>

```sql
CREATE TABLE `appdelivery`.`categorias` (
  `ID` INT NOT NULL,
  `NOME` VARCHAR(30),	
  PRIMARY KEY (`ID`));
  
CREATE TABLE `appdelivery`.`pagamentos` (
  `ID` INT NOT NULL,
  `NOME` VARCHAR(30),	
  PRIMARY KEY (`ID`));
  
CREATE TABLE `appdelivery`.`produtos` (
  `ID` INT NOT NULL,
  `NOME` VARCHAR(30),
  `DESCR` VARCHAR(150),
  `PRECO` DECIMAL(7,2), 
  `IDCATEGO` INT NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT FOREIGN KEY (`IDCATEGO`) REFERENCES `categorias` (`ID`));

CREATE TABLE `appdelivery`.`usuarios` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `NOME` VARCHAR(60),
  `LOGIN` VARCHAR(20),
  `EMAIL` VARCHAR(40), 
  `SENHA` VARCHAR(64),
  PRIMARY KEY (`ID`));
  
CREATE TABLE `appdelivery`.`pedidos` (
  `ID` VARCHAR(5) NOT NULL,
  `CLIENTE` VARCHAR(60),
  `TELEFONE` VARCHAR(15),
  `ENDERECO` VARCHAR(100), 
  `NUM_END` INT,
  `BAIRRO` VARCHAR(60),
  `COMPLEMENTO` VARCHAR(250),
  `REFERENCIA` VARCHAR(250),
  `DT_PEDIDO` DATE, 
  `HORA_PEDIDO` TIME, 
  `VALOR_TOTAL` DECIMAL(7,2), 
  `ID_PAG` INT NOT NULL,
  `STATUS` CHAR(1),
  PRIMARY KEY (`ID`),
  CONSTRAINT FOREIGN KEY (`ID_PAG`) REFERENCES `pagamentos` (`ID`));
  
CREATE TABLE `appdelivery`.`itens_pedido` (
  `ID_PED` VARCHAR(5) NOT NULL,
  `ID_PRODUTO` INT,
  CONSTRAINT FOREIGN KEY (`ID_PED`) REFERENCES `pedidos` (`ID`));
  
CREATE TABLE `appdelivery`.`meio_a_meio` (
  `ID_PED` VARCHAR(5) NOT NULL,
  `ID_PIZZA1` INT,
  `ID_PIZZA2` INT,
  CONSTRAINT FOREIGN KEY (`ID_PED`) REFERENCES `pedidos` (`ID`));
  
CREATE TABLE `appdelivery`.`num_ped` (
  `PEDIDO` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`PEDIDO`));
```
<br>
Para acessar o painel de administração, insira um usuário na tabela de usuário utilizando uma senha em formato de SHA256 que pode ser gerada <a href="https://tools.keycdn.com/sha256-online-generator">aqui</a>, a query deve ficar mais ou menos dessa maneira:
<br><br>

```sql
INSERT INTO USUARIOS VALUES (1,'Administrador','admin','','46070d4bf934fb0d4b06d9e2c46e346944e322444900a435d7d9a95e6d7435f5');
```

Na query acima o SHA256 do campo SENHA refere-se a senha "teste".
</details>
<br>
<strong>Fontes, imagens e icones:</strong>
<br><br>
<ul>
    <li>Fontes Ubuntu e Chelsea Market retirada do <a href="https://fonts.google.com">Google Fonts</a></li>
    <li>Icones de rede sociais e outras imagens retiradas de <a href="https://icons8.com.br/icons">Icons 8</a></li>
    <li>O background do app foi retirado do <a href="https://br.pinterest.com">Pinterest</a> e logotipo do <a href="https://www.gratispng.com">Grátis PNG</a></li>
</ul>

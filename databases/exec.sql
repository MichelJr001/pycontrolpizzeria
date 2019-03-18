/**
DROP TABLE usuarios;
DROP TABLE clientes;
*/

CREATE TABLE usuarios (
	'id_user' INTEGER PRIMARY KEY AUTOINCREMENT,
	'nome' VARCHAR(100) UNIQUE,
	'senha' VARCHAR(100)
);

CREATE TABLE 'clientes' (
	'id_cliente' INTEGER PRIMARY KEY AUTOINCREMENT,
	'nome' VARCHAR(200),
	'telefone' VARCHAR(15),
	'endereço' TEXT,
	'cpf' INT(11) UNIQUE
);
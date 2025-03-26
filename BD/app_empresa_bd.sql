

-- Volcando estructura de base de datos para app_dashboard_flask
CREATE DATABASE IF NOT EXISTS app_empresa_bd; 
USE app_empresa_bd;

-- Volcando estructura para tabla app_dashboard_flask.tbl_conductores
CREATE TABLE IF NOT EXISTS tbl_conductores (
  id_conductor int NOT NULL AUTO_INCREMENT,
  nombre_conductor varchar(50) DEFAULT NULL,
  apellido_conductor varchar(50) DEFAULT NULL,
  sexo_conductor int DEFAULT NULL,
  telefono_conductor varchar(50) DEFAULT NULL,
  email_conductor varchar(50) DEFAULT NULL,
  profesion_conductor varchar(50) DEFAULT NULL,
  foto_conductor mediumtext,
  salario_conductor bigint DEFAULT NULL,
  fecha_registro timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_conductor)
) ;

-- Volcando datos para la tabla app_dashboard_flask.tbl_conductores: ~3 rows (aproximadamente)
INSERT INTO tbl_conductores VALUES (4,'Lisao','Vega',1,'54544454','dev@gmail.com','Ingeniero de Sistemas','fda30f83ebbc4fb1a2ce2609b2b1e34c6614c1dff6e44460b9ba27ed5bb8e927.png',3500000,'2023-08-23 17:04:49'),(5,'Brenda','Viera',2,'323543543','brenda@gmail.com','Dev','22c055aeec314572a0046ec50b84f21719270dac6ea34c91b8380ac289fff9e5.png',1200000,'2023-08-23 17:05:34'),(6,'Alejandro','Torres',1,'324242342','alejandro@gmail.com','Tecnico','7b84aceb56534d27aa2e8b727a245dca9f60156a070a47c491ff2d21da1742e5.png',2100,'2023-08-23 17:06:13'),(7,'Karla','Ramos',2,'345678','karla@gmail.com','Ingeniera','248cc9c38cfb494bb2300d7cbf4a3b317522f295338b4639a8e025e6b203291c.png',2300,'2023-08-23 17:07:28');

-- Volcando estructura para tabla app_dashboard_flask.users
CREATE TABLE IF NOT EXISTS users (
  id int NOT NULL AUTO_INCREMENT,
  name_surname varchar(100)  NOT NULL,
  email_user varchar(50)  NOT NULL,
  pass_user text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  created_user timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ;

-- Volcando datos para la tabla app_dashboard_flask.users: ~2 rows (aproximadamente)
INSERT INTO users (`id`, `name_surname`, `email_user`, `pass_user`, `created_user`) VALUES
  (1, 'ecvega', 'dev@gmail.com', 'scrypt:32768:8:1$ZXqvqovbXYQZdrAB$66758083429739f4f8985992b22cb89fb58c04b99010858e7fb26f73078a23dd3e16019a17bf881108d582a91a635d2c21d26d80da1612c2d9c9bbb9b06452dc', '2023-07-21 20:10:01'),
  (2, 'demo', 'demo@gmail.com', 'scrypt:32768:8:1$Yl2tGU1Ru1Q4Jrzq$d88a0ded538dcfc3a01c8ebf4ea77700576203f6a7cc765f04627464c6047bdcf8eaad84ca3cf0bb5ed058d2dff8ee7a0ba690803538764bedc3ba6173ac6a8a', '2023-07-21 20:29:28');

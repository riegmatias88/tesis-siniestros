#Readme Tesis

#Crear entorno virtual

python3 -m venv tesisUM

cd /Users/mrieg/Desktop/Mati/UM/Tesis
source tesisUM/bin/activate





#Instalar pandas

pip3 install pandas

#Para mapa de calor
pip3 install folium

#extraer requisitos

pip freeze > requirements.txt

pip install -r requirements.txt


pip install pre-commit


#Iniciar git

git init









#Instalar conector mysql
pip install mysql-connector-python

#Instalar mysql
brew install mysql

brew services start mysql

mysql -u root

# Crear base de datos
create database siniestros;

create user siniestros_USER identified by 'user123';

grant all privileges on siniestros.* to 'siniestros_USER'@'%';

flush privileges;

use siniestros;


DROP TABLE IF EXISTS siniestros.siniestro_categoria;
CREATE TABLE siniestros.siniestro_categoria (
	id int,
	descripcion varchar(100),
	PRIMARY KEY (id)
);

Siniestro fatal
Siniestro con lesionados
Siniestro simple
Siniestro sin especificar

INSERT INTO siniestros.siniestro_categoria (id,descripcion) VALUES (1,'Siniestro fatal');
INSERT INTO siniestros.siniestro_categoria (id,descripcion) VALUES (2,'Siniestro con lesionados');
INSERT INTO siniestros.siniestro_categoria (id,descripcion) VALUES (3,'Siniestro simple');
INSERT INTO siniestros.siniestro_categoria (id,descripcion) VALUES (9,'Siniestro sin especificar');


DROP TABLE IF EXISTS siniestros.siniestro_tipo;
CREATE TABLE siniestros.siniestro_tipo (
	id int,
	descripcion varchar(100),
	PRIMARY KEY (id)
);

INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (1,'Atropello a peaton');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (2,'Atropello animal');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (3,'Caída');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (4,'Colisión');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (5,'Despeñamiento');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (6,'Despiste');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (7,'Explosión');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (8,'Incendio');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (9,'Inmersión');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (10,'Choque contra objeto fijo');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (11,'Vuelco');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (12,'Derrape');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (97,'Otro');
INSERT INTO siniestros.siniestro_tipo (id,descripcion) VALUES (99,'Sin dato');



DROP TABLE IF EXISTS siniestros.participantes;
CREATE TABLE siniestros.participantes (
	id int,
	descripcion varchar(100),
	PRIMARY KEY (id)
);

DROP TABLE IF EXISTS siniestros.via_tipo;
CREATE TABLE siniestros.via_tipo (
	id int,
	descripcion varchar(100),
	PRIMARY KEY (id)
);

INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (1,'Autopista');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (2,'Autovía');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (3,'Avenida');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (4,'Calle');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (5,'Camino rural');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (6,'Ruta Nacional');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (7,'Ruta Provincial');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (8,'Ruta sin especificar');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (9,'Puente');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (10,'Autopista Nacional');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (11,'Autopista Provincial');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (12,'Rotonda');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (97,'Otro');
INSERT INTO siniestros.via_tipo (id,descripcion) VALUES (99,'Sin dato');

DROP TABLE IF EXISTS siniestros.via_material;
CREATE TABLE siniestros.via_material (
	id int,
	descripcion varchar(100),
	PRIMARY KEY (id)
);



DROP TABLE siniestros.siniestro;
CREATE TABLE siniestros.siniestro (
    provincia_desc VARCHAR(100),
    departamento_desc VARCHAR(100),
    localidad_desc VARCHAR(100),
    Siniestro_fecha DATE,
    Siniestro_hora TIME,
    Siniestro_franja_horaria_desc VARCHAR(50),
    Siniestro_zona_de_ocurrencia_desc VARCHAR(100),
    Siniestro_tipo_via_publica_id INT,
    Siniestro_via VARCHAR(100),
    Siniestro_altura INT,
    Siniestro_inteseccion VARCHAR(100),
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    categoria_del_Siniestro_id INT,
    tipo_Siniestro1_id INT,
    tipo_Siniestro2_id INT,
    tipo_Siniestro3_id INT,
    Vehiculo INT,
    Interviniente_Automóvil INT,
    Interviniente_Motovehiculo INT,
    Interviniente_Peatón INT,
    Interviniente_Bicicleta INT,
    Interviniente_Cuatriciclo INT,
    Interviniente_Camioneta_Utilitario INT,
    Interviniente_Transporte_de_carga INT,
    Interviniente_Transporte_de_pasajeros INT,
    Interviniente_Maquinaria INT,
    Interviniente_Tracción_a_sangre INT,
    Interviniente_veh_mov_personal INT,
    Interviniente_tren INT,
    Interviniente_Vehículo_oficial INT,
    Interviniente_Otro INT,
    Interviniente_Sin_datos INT
);


ALTER TABLE siniestros.siniestro 
ADD PRIMARY KEY (Siniestro_fecha, Siniestro_hora, latitud, longitud);

ALTER TABLE siniestros.siniestro
ADD FOREIGN KEY (Siniestro_tipo_via_publica_id) REFERENCES via_tipo(id);

ALTER TABLE siniestros.siniestro
ADD FOREIGN KEY (tipo_Siniestro1_id) REFERENCES siniestro_tipo(id);

ALTER TABLE siniestros.siniestro
ADD FOREIGN KEY (tipo_Siniestro2_id) REFERENCES siniestro_tipo(id);

ALTER TABLE siniestros.siniestro
ADD FOREIGN KEY (tipo_Siniestro3_id) REFERENCES siniestro_tipo(id);

ALTER TABLE siniestros.siniestro
ADD FOREIGN KEY (categoria_del_Siniestro_id) REFERENCES siniestro_categoria(id);


--DEPURO DATOS INVALIDOS

DELETE FROM siniestro where Siniestro_fecha = '1970-01-01';

--DEPURO DATOS DUPLICADOS

Paso 1)

SELECT Siniestro_fecha, Siniestro_hora, latitud, longitud, COUNT(*)
FROM siniestro
GROUP BY Siniestro_fecha, Siniestro_hora, latitud, longitud
HAVING COUNT(*) > 1;


Paso 2)

CREATE TEMPORARY TABLE temp_table AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY Siniestro_fecha, Siniestro_hora, latitud, longitud ORDER BY Siniestro_fecha) AS row_num
    FROM siniestro
) sub
WHERE row_num = 1;


Paso 3)

DELETE FROM siniestro
WHERE (Siniestro_fecha, Siniestro_hora, latitud, longitud) NOT IN (
    SELECT Siniestro_fecha, Siniestro_hora, latitud, longitud
    FROM temp_table
);


Paso 4)

TRUNCATE TABLE siniestro;

INSERT INTO siniestro
SELECT provincia_desc, departamento_desc, localidad_desc, Siniestro_fecha, Siniestro_hora, Siniestro_franja_horaria_desc, Siniestro_zona_de_ocurrencia_desc, Siniestro_tipo_via_publica_id, Siniestro_via, Siniestro_altura, Siniestro_inteseccion, latitud, longitud, categoria_del_Siniestro_id, tipo_Siniestro1_id, tipo_Siniestro2_id, tipo_Siniestro3_id, Vehiculo, Interviniente_Automóvil, Interviniente_Motovehiculo, Interviniente_Peatón, Interviniente_Bicicleta, Interviniente_Cuatriciclo, Interviniente_Camioneta_Utilitario, Interviniente_Transporte_de_carga, Interviniente_Transporte_de_pasajeros, Interviniente_Maquinaria, Interviniente_Tracción_a_sangre, Interviniente_veh_mov_personal, Interviniente_tren, Interviniente_Vehículo_oficial, Interviniente_Otro, Interviniente_Sin_datos
FROM temp_table;












Test
select * from siniestro where categoria_del_Siniestro_id = 9;


cat Siniestros.csv | grep "Ciudad Autónoma de Buenos Aires" > Siniestros_2.csv
head -50000 Siniestros.csv > Siniestros_2.csv
python3 ./mapa.py


-21.77,-66.2. AL NORTE


Y,X

select latitud,longitud,provincia_desc from siniestro where latitud > -21;

select latitud,longitud,provincia_desc from siniestro where longitud > -40;


--Clima



CREATE TABLE `clima` (
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `temp` int DEFAULT NULL,
  `viento_rafaga` int DEFAULT NULL,
  `viento_velocidad` int DEFAULT NULL,
  `nubosidad_porc` int DEFAULT NULL,
  `precip_mm` float DEFAULT NULL
);


CREATE TABLE `clima` (
  `fecha` date,
  `hora` time,
  `value` int);


ALTER TABLE temperatura ADD COLUMN wind_gusts int;

UPDATE temperatura t
JOIN wind_gusts wg ON t.fecha = wg.fecha and t.hora = wg.hora
SET t.wind_gusts = wg.value;


ALTER TABLE temperatura ADD COLUMN wind_speed int;

UPDATE temperatura t
JOIN wind_speed ws ON t.fecha = ws.fecha and t.hora = ws.hora
SET t.wind_speed = ws.value;

ALTER TABLE temperatura ADD COLUMN rain float;


UPDATE temperatura t
JOIN rain r ON t.fecha = r.fecha and t.hora = r.hora
SET t.rain = r.value;

ALTER TABLE temperatura ADD COLUMN cloud int;

UPDATE temperatura t
JOIN cloud c ON t.fecha = c.fecha and t.hora = c.hora
SET t.cloud = c.value;


ALTER TABLE temperatura RENAME COLUMN temperatura TO temp;
ALTER TABLE temperatura RENAME COLUMN wind_gusts TO viento_rafaga;
ALTER TABLE temperatura RENAME COLUMN wind_speed TO viento_velocidad;
ALTER TABLE temperatura RENAME COLUMN nubosidad TO nubosidad_porc;
ALTER TABLE temperatura RENAME COLUMN precip TO precip_mm;

RENAME TABLE temperatura TO clima;


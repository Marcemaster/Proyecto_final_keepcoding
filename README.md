# Proyecto_final_keepcoding

*Proyecto fin Bootcamp Aprender a programar desde cero*


El proyecto consiste en una calculadora de inversión en criptomonedas que calcula el resultado a tiempo real a través de la Api de CoinApi


# Instrucciones de uso:

## Instalar dependencias 

```
pip install -r requierements.txt
```

## Crear base de datos

Dentro de una caprpeta "data" escribe en el terminal:

```
sqlite3 movimientos.db
```

Copia el código que está en la carpeta migrations en la consola:

```
CREATE TABLE "movimientos" (
	"id"	INTEGER,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"moneda_from"	TEXT NOT NULL,
	"cantidad_from"	REAL NOT NULL,
	"moneda_to"	TEXT NOT NULL,
	"cantidad_to"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
```

## .env_template

Cambia el nombre a .env_template por .env y selecciona el modo en FLASK_ENV


## Config.py

Cambia el nombre al archivo config_template.py por config.py e introduce la API_KEY que has obtenido previamente en [CoinApi.io](https://www.coinapi.io/)

Si has creado la carpeta con otro nombre, introduce la dirección en DATABASE


## Inicio

Para probar la aplicación escribe en tu terminal:

```
flask run
```


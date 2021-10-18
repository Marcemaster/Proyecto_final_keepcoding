from programa import app
from flask import render_template, request, redirect, url_for, flash, jsonify
from programa.models import DBManager, consultaApi
from datetime import date
from config import DATABASE, API_KEY

consultaapi = consult
dbmanager = DBManager("data/movimientos.db")
url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol={}&convert={}&CMC_PRO_API_KEY={}'


@app.route("/")
def inicio():

    consulta = '''SELECT *
                 FROM movimientos 
                ORDER BY date;'''

    movimientos = dbmanager.consultaSQL(consulta)
    return render_template("index.html", items=movimientos)


@app.route("/api/v1/movimientos")
def lista_movimientos():

    consulta = '''SELECT *
                 FROM movimientos 
                ORDER BY date;'''
    movimientos = dbmanager.consultaSQL(consulta)

    resultados = {
        "status": "success",
        "movimientos": movimientos
    }

    return jsonify(resultados)

# Creando la nueva ruta para el ID del movimiento

@app.route("/api/v1/movimiento/<int:id>", methods=["GET"])
def movimiento(id):
    try:
        consulta_movimiento = '''SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to
                                FROM movimientos
                                WHERE id = ?;'''

        movimiento = dbmanager.consultaSQL(consulta_movimiento, [id])

        if len(movimiento) == 0:
            error = {
            "status": "fail",
            "message": "Movimiento no encontrado"
            }
            return jsonify(error), 400
        
        return jsonify(movimiento)  

    except Exception as error:
        error = {
            "status": "fail",
            "message": str(error)
            }
        return jsonify(error), 400


@app.route("/api/v1/movimiento", methods=["POST"])
def nuevo_movimiento():

    try:
        consulta = '''INSERT INTO 
                    movimientos 
                    (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) 
                    values 
                    (:date, :time, :moneda_from, :cantidad_from, :moneda_to, :cantidad_to)
                    '''

        dbmanager.modificaSQL(consulta, request.json)
        return jsonify({"status": "success"})

    except Exception as error:
        error = {
            "status": "fail",
            "message": str(error)
            }
        return jsonify(error), 400

def calcular_tasa_cambio():
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'

    parameters = {
        'amount':cantidad_from,
        'symbol': moneda_from,
        'convert': moneda_to
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        precio_cambio = data['data']['quote'][moneda_to]['price']
        return precio_cambio

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        pprint.pprint(e)
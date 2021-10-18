from programa import app
from flask import render_template, request, jsonify
from programa.models import DBManager, consultaApi
from config import DATABASE, API_KEY

# TODO falta chequear el saldo antes de postear un movimiento
# TODO falta la vista de status


# consultaapi = consult
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
    try:
        consulta = '''SELECT *
                    FROM movimientos 
                    ORDER BY date;'''
        movimientos = dbmanager.consultaSQL(consulta)

        resultados = {
            "status": "success",
            "movimientos": movimientos
        }

        return jsonify(resultados)

    except Exception as error:
        error = {
            "status": "fail",
            "message": str(error)
        }
        return jsonify(error), 400


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

    if request.json["message"] == "compra":

        if request.json["moneda_from"] != "EUR":
            balance = comprobar_balance(request.json["cantidad_from"])

            if balance >= float(request.json["cantidad_from"]):
                return request_Api()

            else:
                error = {
                    "status": "fail",
                    "message": "Balance insuficiente"
                }
                return jsonify(error), 200
        else:
            return request_Api()

    else:
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


def comprobar_balance(moneda):
    comprobar_comprado = f''' SELECT IFNULL (SUM(cantidad_to), 0) FROM movimientos WHERE moneda_to = "{moneda}";'''
    comprobar_vendido = f''' SELECT IFNULL (SUM(cantidad_from), 0) FROM movimientos WHERE moneda_from = "{moneda}";'''

    total_comprado = dbmanager.consultaBalanceSQL(comprobar_comprado)
    total_vendido = dbmanager.consultaBalanceSQL(comprobar_vendido)

    balance = total_comprado - total_vendido

    return balance


def request_Api():
    try:
        request_api = float(request_api.consulta_tasa(request.json["moneda_from"], request.json["moneda_to"]))
        respuesta = {
            "status": "succes",
            "cantidad_to": request_api * float(request.json["cantidad_from"]),
            "precio_unitario": request_api
        }

        return jsonify(respuesta), 201

    except Exception as error:
        error = {
            "status": "fail",
            "message": str(error)
        }
        return jsonify(error), 400


def status_inversion():

    consulta = '''SELECT * 
                FROM investments 
                ORDER BY date;'''
    try:
        criptos = dbmanager.obtenerMonedas(consulta)
        monedas = "EUR,"

        for moneda in criptos:
            monedas += f"{moneda}"

        










def calcular_tasa_cambio():
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'

    parameters = {
        'amount': cantidad_from,
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

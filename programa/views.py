from programa import app
from flask import render_template, request, jsonify
from programa.models import DBManager, consultaApi
from config import DATABASE


dbmanager = DBManager("data/movimientos.db")

url = 'https://rest.coinapi.io/v1/exchangerate/{}/{}'
consulta_api = consultaApi(url)

url_status = 'https://rest.coinapi.io/v1/assets/{}'
consulta_estado_api = consultaApi(url_status)



@app.route("/")
def inicio():
    return render_template("index.html")


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


    except Exception as error:
        error = {
            "status": "fail",
            "message": str(error)
        }
        return jsonify(error), 400

    return jsonify(resultados)


@app.route("/api/v1/movimientos/<int:id>", methods=['GET'])
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


@app.route("/api/v1/movimiento", methods=['POST'])
def nuevo_movimiento():
    if request.json["message"] == "convert":

        if request.json["moneda_from"] != 'EUR':
            balance = comprobar_balance(request.json["moneda_from"])

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
    comprobar_comprado = f''' SELECT IFNULL(SUM(cantidad_to), 0) FROM movimientos WHERE moneda_to = "{moneda}";'''
    comprobar_vendido = f''' SELECT IFNULL(SUM(cantidad_from), 0) FROM movimientos WHERE moneda_from = "{moneda}";'''

    total_comprado = dbmanager.consultaBalanceSQL(comprobar_comprado)
    total_vendido = dbmanager.consultaBalanceSQL(comprobar_vendido)

    balance = total_comprado - total_vendido

    return balance


def request_Api():

    try:
        request_coinapi = float(consulta_api.consulta_tasa(request.json["moneda_from"], request.json["moneda_to"]))
        respuesta = {
            "status": "success",
            "cantidad_to": request_coinapi * float(request.json["cantidad_from"]),
            "precio_unitario": request_coinapi
        }
        return jsonify(respuesta), 201

    except Exception as error:
        error = {
            "status": "fail",
            "message": str(error)
        }
        return jsonify(error), 400

@app.route("/api/v1/status")
def status_inversion():
    try:
        comprobar_balance_from = ''' SELECT IFNULL(SUM (cantidad_from), 0) FROM movimientos WHERE moneda_from = "EUR";'''
        inversion_from = dbmanager.consultaBalanceSQL(comprobar_balance_from)

        comprobar_balance_to =''' SELECT IFNULL(SUM (cantidad_to),0) FROM movimientos WHERE moneda_to = "EUR";'''
        inversion_to = dbmanager.consultaBalanceSQL(comprobar_balance_to)

        criptos = dbmanager.obtenerMonedas('''SELECT * FROM movimientos ORDER BY date;''')
        monedas = "EUR,"

        if criptos != []:
            for m in criptos:
                monedas += f"{m},"
            
            valores_dolares = consulta_estado_api.consulta_status(monedas)
            total_dolares = 0

            for moneda in criptos:
                balance = comprobar_balance(moneda)
                total_dolares_moneda = balance * valores_dolares[f"{moneda}"]
                total_dolares += total_dolares_moneda
        
            inversion = inversion_from - inversion_to
            print(valores_dolares["EUR"])
            total = total_dolares / valores_dolares["EUR"]
            resultado = total - inversion

        else:
            inversion = 0
            total = 0
            resultado = 0


        # LO ÚLTIMO QUE HE HECHO HA SIDO IGUALAR LA INVERSIÓN A INVERSION_FROM EN LUGAR DE INVERSIÓN PARA QUE NO SE QUEDE EN NEGATIVO CUANDO TIENES BENEFICIO
        respuesta = {
            "status":"success",
            "data": {"inversion": inversion_from, "total": total, "resultado":resultado}
        }
        return jsonify(respuesta), 200

    except Exception as error:
        error = {
            "status": "fail",
            "message": str(error)
        }
        return jsonify(error), 400


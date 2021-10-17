from programa import app
from flask import render_template, request, redirect, url_for, flash, jsonify
from programa.models import DBManager
from datetime import date


dbmanager = DBManager("data/movimientos.db")

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


@app.route("/api/v1/movimiento", methods=["POST"])
def modifica_movimiento():
    
    consulta = '''INSERT INTO 
                movimientos 
                (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) 
                values 
                (:date, :time, :moneda_from, :cantidad_from, :moneda_to, :cantidad_to)'''

    dbmanager.modificaSQL(consulta, request.json)
    return jsonify({"status": "success"})


    # Esto es una probatina a ver qué tal sale

    #@app.route("/api/v1/movimiento", methods=["GET","POST"])
    #pass

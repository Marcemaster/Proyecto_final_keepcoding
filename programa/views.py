from programa import app
from flask import render_template, request, redirect, url_for, flash
from programa.models import MovimientoFormulario
from datetime import date



@app.route("/")
def inicio():

    consulta = '''SELECT *
                 FROM movimiento 
                ORDER BY fecha;'''
    movimientos = dbmanager.consultaSQL(consulta)
    return render_template("index.html")

from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, FloatField, RadioField, SubmitField, StringField


#Estos validadores habrá que usarlos en el momento de la gestión de errores

from wtforms.validators import DataRequired, Length, NumberRange
import datetime

# def validar_fecha(formulario, campo):
  #  hoy = datetime.date.today()
   # if campo.data > hoy:
    #    raise ValidationError("La fecha no puede ser posterior a hoy")

class MovimientoFormulario(FlaskForm):


#Trabajo pendiente. Incluir validadores de los campos del formulario. Especial atención en el campo "fecha" ya que hay que darle formato YY/MM/etc..
    id = HiddenField()
    date = DateField("Fecha", valida)
    time =
    moneda_from =
    cantidad_from = 
    moneda_to =
    cantidad_to = 
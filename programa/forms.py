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

    # Pendiente cambiar formato de fecha YYYY/MM/DD y time para las horas HH/SS/MM etc como marca en la descripción del proyecto.
    date = DateField("Fecha", validators = [DataRequired(message="Debe informar la fecha")])
    time = DateField("Fecha", validators = [DataRequired(message="Debe informar la fecha")])

    # Más adelante cambiar los campos moneda_from y moneda_to por unos SelectField, que funcionan con tuplas de clave-valor.
    moneda_from = StringField("Moneda de origen", validators=[DataRequired(message="Debe informar la moneda de orgen")])
    cantidad_from = FloatField("Cantidad de origen", validators=[DataRequired(message="Debe informar la cantidad de origen"), NumberRange(min=0.01)])
    moneda_to = StringField("Moneda de origen", validators=[DataRequired(message="Debe informar la moneda de orgen")])
    cantidad_to = FloatField("Cantidad de origen", validators=[DataRequired(message="Debe informar la cantidad de origen")])

    submit = SubmitField("Aceptar")
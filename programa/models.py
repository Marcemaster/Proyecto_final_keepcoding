import sqlite3
import requests
from config import API_KEY

# Estas funciones son las que actualizan la BBDD y consultan a la API, trabajan en el backend y se conectan a través del fichero views.py

class DBManager():
    def __init__(self, ruta_basedatos):
        self.ruta_basedatos = ruta_basedatos

    def consultaSQL(self, consulta, params=[]):
        conexion = sqlite3.connect(self.ruta_basedatos)

        cur = conexion.cursor()
        cur.execute(consulta, params)

        keys = []
        for item in cur.description:
            keys.append(item[0])

        registros = []
        for registro in cur.fetchall():
            ix_clave = 0
            d = {}
            for columna in keys:
                d[columna] = registro[ix_clave]
                ix_clave += 1
            registros.append(d)

        conexion.close()
        return registros

    def modificaSQL(self, consulta, params):
        conexion = sqlite3.connect(self.ruta_basedatos)

        cur = conexion.cursor()
        cur.execute(consulta, params)
        conexion.commit()
        conexion.close()
 
    def consultaBalanceSQL(self, consulta, params):
        conexion = sqlite3.connect(self.ruta_basetdatos)

        cur = conexion.cursor()

        cur.execute(consulta, params)
        suma_total = cur.fetchone()[0]

        conexion.close()
        return total_sum

    def obtenerMonedas(self, consulta, params = []):

        movimientos = self.querySQL(consulta)
    
        monedas = []
        for mov in movimientos:
            if mov["moneda_from"] not in monedas and mov["moneda_from"] != "EUR":
                monedas.append(mov["moneda_from"])
            if mov["currency_to"] not in monedas and mov["moneda_to"] != "EUR":
                monedas.append(mov["moneda_to"])
        return monedas

class consultaApi():
    def __init__(self, url, params = []):
        self.url = url

    def consulta_tasa(self, moneda_from, moneda_to):
        headers = {'X-CMC_PRO_API_KEY': API_KEY}
        self.moneda_from = moneda_from
        self.moneda_to = moneda_to
        request = requests.get((self.url).format(self.moneda_from, self.moneda_to), headers = headers)

        return request.json()["price"]

    def consulta_status(self, params):
        headers = {'X-CoinAPI-Key': API_KEY}
        self.params = params

        request = request.get((self.url).format(self.params), headers = headers)
        diccionario_valores_USD = request.json()

        diccionario_valores = {}
        for moneda in diccionario_valores_USD:
            # HAY QUE REPASAR LA LINEA 76
            diccionario_valores.update({moneda['asset_id']:moneda['price_usd']})

        return diccionario_valores

# TODO pendiente borrar esta función.
def obtenerCantidad_to(moneda_from,cantidad_from, moneda_to):

  url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'

 # cantidad_from
 # moneda_from = 'BTC'
 # moneda_to = 'EUR'

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
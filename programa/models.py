import sqlite3


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


# Conversión de monedas 


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
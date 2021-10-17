
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
from config import API_KEY

LISTA_SYMBOLS= ["EUR","BTC","ETH","XRP","LTC","BCH","BNB","USDT","EOS","BSV","XLM","ADA","TRX"]



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

cambio = obtenerCantidad_to('BTC',1, 'EUR')
print(cambio) 
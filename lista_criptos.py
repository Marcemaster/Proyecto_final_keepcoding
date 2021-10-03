
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
from config import API_KEY

lista_id = []
lista_slugs = []
lista_symbols = []
lista_name = []

monedas_ids = {}

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
parameters = {
  'start':'1',
  'limit':'12',
  'symbol': 'UR,BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX',
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

    for i in range(12):
        monedas_ids[data['data'][i]['name']] = data['data'][i]['id']

except (ConnectionError, Timeout, TooManyRedirects) as e:
    pprint.pprint(e)

pprint.pprint(monedas_ids)
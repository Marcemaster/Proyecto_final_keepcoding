
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
from config import API_KEY

lista_id = []
lista_slugs = []
lista_symbols = []
lista_name = []

#,BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX

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
    pprint.pprint(data['data'][0]['id'])
    #lista_id.append(data['platform']['id'])
#
    #pprint.pprint(data['platform']['name'])
    #lista_name.append(data['platform']['name'])
#
    #pprint.pprint(data['platform']['symbol'])
    #lista_symbols.append(data['platform']['symbol'])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    pprint.pprint(e)
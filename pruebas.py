from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from config import API_KEY
import pprint

ID_list = [1]
for i in ID_list:
    i = str(i)
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
    'id': f"{i}",
    'convert':'EUR'
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
        pprint.pprint(data['data'][i]['name']+': ' + str((data['data'][i]['quote']['EUR']['price'])))
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)



'''
ESTO ESTABA EN INDEX HTML Y LLAMABAMOS A LA LISTA DE MOVIMIENTOS DESDE PYTHON VIEWS. COMO LO HACEMOS CON JS ESTO SOBRA PERO POR SI ACA

                <tr>
                    <td>{{ item.date }}</td>
                    <td>{{ item.time }}</td>
                    <td>{{ item.moneda_from }}</td>
                    <td>{{ item.cantidad_from }}</td>
                    <td>{{ item.moneda_to }}</td>
                    <td>{{ item.cantidad_to }}</td>
                </tr>
                {% endfor %}
'''
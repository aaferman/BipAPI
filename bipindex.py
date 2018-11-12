from flask import Flask
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json

app = Flask(__name__)

@app.route('/<int:bip_id>')
def get_info(bip_id):

    bip_data = {}
    bip_data['ID'] = bip_id
    bip_data['current_count'] = get_balance(bip_id)
    bip_data['payments'] = get_payments(bip_id)

    return json.dumps(bip_data, sort_keys=True, indent=4, separators=(',', ': '))


def get_balance(bip_id):

    url = 'http://bip-servicio.herokuapp.com/api/v1/solicitudes.json'
    params = dict(
        bip=bip_id
    )
    resp = requests.get(url=url, params=params)
    data = resp.json()

    return data['saldoTarjeta']


def get_payments(bip_id):
    driver = webdriver.Firefox()

    driver.get(f'http://pocae.tstgo.cl/PortalCAE-WAR-MODULE/SesionPortalServlet?accion=6&NumDistribuidor=99&NomUsuario=usuInternet&NomHost=AFT&NomDominio=aft.cl&Trx=&RutUsuario=0&NumTarjeta={bip_id}&bloqueable=')

    driver.find_element_by_link_text("Saldo y Movimientos").click()

    html = driver.page_source

    soup = BeautifulSoup(html)

    payments = dict()

    count = 0

    for row in soup.find_all('table')[2].find_all('table')[4].find_all('table')[7].find_all('tr'):
        for row2 in row.find_all('td'):
            if row2.text == 'Carga Tarjeta':
                payment = {'date': row2.parent.find_all('td')[3].text, 'amount': row2.parent.find_all('td')[5].text}
                payments[count] = payment
                count += 1

    driver.quit()

    return payments

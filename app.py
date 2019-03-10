from flask import Flask
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import os
import redis

app = Flask(__name__)


@app.route('/')
def index():
    return 'Readme at <a href="https://github.com/aaferman/BipAPI/">https://github.com/aaferman/BipAPI/</a>'


@app.route('/<int:bip_id>')
def get_info(bip_id):
    print('Request: ' + str(bip_id))
    db = redis.from_url(os.environ.get("REDIS_URL"))
    if (db.get(bip_id)):
        return json.dumps(json.loads(db.get(bip_id)), sort_keys=True, indent=4, separators=(',', ': '))

    bip_data = {}
    bip_data['ID'] = bip_id
    bip_data['current_balance'] = get_balance(bip_id)
    bip_data['payments'] = get_payments(bip_id)[0]
    bip_data['uses'] = get_payments(bip_id)[1]

    db.set(bip_id, json.dumps(bip_data))

    return json.dumps(bip_data, sort_keys=True, indent=4, separators=(',', ': '))


def get_balance(bip_id):

    url = 'http://bip-servicio.herokuapp.com/api/v1/solicitudes.json'
    params = dict(
        bip=bip_id
    )
    resp = requests.get(url=url, params=params)
    data = resp.json()

    return int((data['saldoTarjeta']).replace(u'.', u'').replace(u'$', u''))


def get_payments(bip_id):

    if 'ENV' in os.environ and os.environ['ENV'] == 'HEROKU':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ['GOOGLE_CHROME_BIN']
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], chrome_options=chrome_options)
    else:
        driver = webdriver.Chrome()

    driver.get(f'http://pocae.tstgo.cl/PortalCAE-WAR-MODULE/SesionPortalServlet?accion=6&NumDistribuidor=99&NomUsuario=usuInternet&NomHost=AFT&NomDominio=aft.cl&Trx=&RutUsuario=0&NumTarjeta={bip_id}&bloqueable=')

    driver.find_element_by_link_text("Saldo y Movimientos").click()

    html = driver.page_source

    soup = BeautifulSoup(html, features="html.parser")

    payments = dict()
    uses = dict()

    payment_count = 0
    use_count = 0

    for row in soup.find_all('table')[2].find_all('table')[4].find_all('table')[7].find_all('tr'):
        for row2 in row.find_all('td'):
            if row2.text == 'Carga Tarjeta':
                payment = {'date': row2.parent.find_all('td')[3].text.replace(u'\xa0', u''), 'amount': int(row2.parent.find_all('td')[5].text.replace(u'\xa0', u'').replace(u'.', u''))}
                payments[payment_count] = payment
                payment_count += 1
            if row2.text == 'Uso Tarjeta':
                use = {'date': row2.parent.find_all('td')[3].text.replace(u'\xa0', u''), 'amount': int(row2.parent.find_all('td')[5].text.replace(u'\xa0', u'').replace(u'.', u'')), 'place': row2.parent.find_all('td')[4].text.replace(u'\xa0', u'')}
                uses[use_count] = use
                use_count += 1

    driver.quit()

    return payments, uses


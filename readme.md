SERVICES
DOCUMENTS
BipAPI.md
SAVE TO 
IMPORT FROM 
DOCUMENT NAME

BipAPI.md
WORDS: 153CHARACTERS: 1197
MARKDOWN Toggle Zen ModePREVIEW Toggle Mode

  
BipAPI
BipAPI is a web scraper that exposes a Rest API to access Chile’s public transport Bip! card’s history.

Currently live at bipapi.herokuapp.com

Installation
BipAPI requires Python3.7 to run.

Install Python and Pip on MacOS using brew.

$ brew install python
Create a virtual enviroment and install dependencies.

$ cd BipAPI
$ python3 virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt 
You may need to also install Selenium Web Driver and Chrome

API Resources
GET /[bip_id]
Response body:

{
"ID": 77033070,
"current_balance": 13090,
"payments": {
    "0": {
        "amount": 5000,
        "date": "27/09/2018 14:47"
    },
    "1": {
        "amount": 5000,
        "date": "08/09/2018 16:04"
    }
},
"uses": {
    "0": {
        "amount": 700,
        "date": "23/10/2018 14:03",
        "place": "Universidad Catolica"
    },
    "1": {
        "amount": 680,
        "date": "28/09/2018 09:34",
        "place": "Pedro de Valdivia"
    },
    "2": {
        "amount": 680,
        "date": "27/09/2018 14:47",
        "place": "El Golf"
    },
    "3": {
        "amount": 680,
        "date": "27/09/2018 13:05",
        "place": "Pedro de Valdivia"
    }
}
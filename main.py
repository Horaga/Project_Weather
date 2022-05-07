import requests
import json
from datetime import datetime
import pandas as pd
import numpy as np



cidades = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes/3513/municipios"
resultCidade = requests.get(cidades)
CHAVE = "b9e1d7b5ce0e14873b69f59f7facdd3d"

bigdata = list()
for x in resultCidade.json():
    CIDADE = x["nome"]
    ESTADO = x["microrregiao"]["mesorregiao"]["UF"]["nome"]
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={CIDADE},{ESTADO}&appid={CHAVE}&units=metric&lang=pt_br"

    result = requests.get(URL)
    jsonDados = result.json()
    saida = {
        "city": CIDADE,
        "state": ESTADO,
        "date": datetime.fromtimestamp(jsonDados['dt']),
        "temp": jsonDados['main']['temp'],
        "min": jsonDados['main']['temp_min'],
        "max": jsonDados['main']['temp_max'],
        "pressure": jsonDados['main']['pressure'],
        "humidity": jsonDados['main']['humidity'],
        "sea_level": jsonDados['main'].get('sea_level') or "",
        "wind": jsonDados['wind']['speed'],
        "weather_main": jsonDados['weather'][0]['main'],
        "weather_description": jsonDados['weather'][0]['description'],
        "weather_icon": jsonDados['weather'][0]['icon']
    }
    # print(saida)
    bigdata.append(saida)
dfs =  pd.DataFrame(bigdata)
print(dfs)
dfs.to_excel("PrevisaoTempo.xlsx")
dfs.to_csv("PrevisaoTempo.csv")
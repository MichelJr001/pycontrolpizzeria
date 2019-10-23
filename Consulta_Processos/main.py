# -*- coding: UTF-8 -*-

import requests
 
url = 'https://www.google.com'
pesquisa = {'q':'python'}

r = requests.post(url,pesquisa)

with open('Resultado_Testes.html', 'w') as f:
    f.write((r.content).decode('utf-8'))

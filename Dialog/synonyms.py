#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def get_sinonimos(queryword):


    ########################### www.sinônimo.com ###########################

    r = requests.get('http://www.xn--sinnimo-v0a.com/busca.html?Search%5Bsection%5D=&Search%5Bsection%5D=S&Search%5Bword%5D='+queryword+'&Search%5Bcontained%5D=0')
    soup = BeautifulSoup(r.text, "lxml")

    try:
        palavras = soup.p.text
    except AttributeError:
        # 404 ou não tem sinónimos
        print('Erro 404')

    lista = palavras.split(", ")


    return lista


if __name__ == "__main__":
    import sys
    print(get_sinonimos(sys.argv[1]))
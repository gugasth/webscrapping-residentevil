# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
# %%
def get_content(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    resp = requests.get(url, headers=headers)
    return resp

def get_basic_infos(soup):
    div = soup.find('div', class_ = 'td-page-content')
    paragrafo = div.find_all('p')[1]
    ems = paragrafo.find_all('em')
    data = {}
    for i in ems:
        chave, valor = i.text.split(':')
        chave = chave.strip(' ')
        data[chave] = valor.strip(' ')
    return data

def get_aparicoes(soup):
    lis = (soup.find('div', class_ = 'td-page-content')
            .find('h4')
            .find_next()
            .find_all('li'))

    aparicoes = [i.text for i in lis]
    return aparicoes

def get_links():
    url = 'https://www.residentevildatabase.com/personagens/'
    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find('div', class_='td-page-content')
               .find_all('a'))
    links = [i['href'] for i in ancoras]
    return links

def get_personagem_infos(url):
    url = 'https://www.residentevildatabase.com/personagens/ada-wong/'

    resp = get_content(url)

    if resp.status_code != 200:
        print('Não foi possível obter os dados!')
    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data['Aparicoes'] = get_aparicoes(soup)
    return data


# %%
links = get_links()
data = []
for i in tqdm(links):
    d = get_personagem_infos(i)
    d["Link"] = i
    nome = i.strip("/").split("/")[-1].replace("-", " ").title()
    d["Nome"] = nome
    data.append(d)


# %%
df = pd.DataFrame(data)
df.to_csv('personagens.csv', index=False)
# %%

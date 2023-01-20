import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

query = 'iphone'.replace(' ', '+')
base_url = 'https://www.amazon.com/s?k={0}'.format(query)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'pt-BR, pt;q=0.5'
}

print('Iniciando a busca...')

response = requests.get(base_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
    
results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

products = []

for result in results:
    product_name = result.h2.text

    try:
        rating = result.find('i', {'class': 'a-icon'}).text
    except AttributeError:
        continue

    try:
        whole_price = result.find('span', {'class': 'a-price-whole'}).text
        fraction_price = result.find('span', {'class': 'a-price-fraction'}).text
        full_price = whole_price + fraction_price

        formatted_price = 'R$ ' + full_price.replace('.', ',')
        products.append([product_name, formatted_price])
    except AttributeError:
        continue
    
df = pd.DataFrame(products, columns=['Nome', 'Valor'])
df.to_csv('{0}.csv'.format('iPhones na Amazon'), index=False)

print('\nBusca finalizada. Planilha salva.')
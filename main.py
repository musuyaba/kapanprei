import requests
from bs4 import BeautifulSoup

url = 'https://tanggalan.com/2024'

response = requests.get(url)
response.raise_for_status() 

soup = BeautifulSoup(response.content, 'html.parser')

uls = soup.find_all('ul')

for ul in uls:
    last_li = ul.find_all('li')[-1]
    
    tables = last_li.find_all('table')
    
    for table in tables:
        trs = table.find_all('tr')
        
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) >= 2:
                date = tds[0].get_text()
                holiday_name = tds[1].get_text()
                print(f'Date: {date}, Holiday: {holiday_name}')

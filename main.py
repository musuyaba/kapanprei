import requests
from bs4 import BeautifulSoup
import json
import re

year = 2024
url = f"https://tanggalan.com/{year}"

response = requests.get(url)
response.raise_for_status() 

soup = BeautifulSoup(response.content, 'html.parser')

holidays = []

uls = soup.find_all('ul')

for ul in uls:
    first_li = ul.find_all('li')[0]
    month_year = first_li.find('a').get_text().strip()
    print(month_year)
    match = re.match(r'([a-zA-Z]+)(\d+)', month_year)
    if match:
        month = match.group(1)
        year = match.group(2)

    last_li = ul.find_all('li')[-1]
    
    tables = last_li.find_all('table')
    
    for table in tables:
        trs = table.find_all('tr')
        
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) >= 2:
                date = tds[0].get_text()
                holiday_name = tds[1].get_text()
                holidays.append({'month': month, 'year': year, 'date': date, 'holiday': holiday_name})


# Save the holidays data to a JSON file
with open(f'{year}.json', 'w', encoding='utf-8') as json_file:
    json.dump(holidays, json_file, ensure_ascii=False, indent=4)

print(f'Holidays data saved to {year}.json')
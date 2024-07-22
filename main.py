import requests
from bs4 import BeautifulSoup
import json
import re
from maps import month_map
from arguments import get_year

year = get_year()
url = f"https://tanggalan.com/{year}"

response = requests.get(url)
response.raise_for_status() 

soup = BeautifulSoup(response.content, 'html.parser')

holidays = []

uls = soup.find_all('ul')

for ul in uls:
    first_li = ul.find_all('li')[0]
    month_year = first_li.find('a').get_text().strip()
    match = re.match(r'([a-zA-Z]+)(\d+)', month_year)
    if match:
        month_name = match.group(1).lower()
        year = match.group(2)

        month = month_map.get(month_name)

    last_li = ul.find_all('li')[-1]
    
    tables = last_li.find_all('table')
    
    for table in tables:
        trs = table.find_all('tr')
        
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) >= 2:
                date = tds[0].get_text()
                holiday_name = tds[1].get_text()
                formatted_date = f'{year}-{month}-{date.zfill(2)}'
                holidays.append({'date': formatted_date, 'holiday': holiday_name})


# Save the holidays data to a JSON file
with open(f'{year}.json', 'w', encoding='utf-8') as json_file:
    json.dump(holidays, json_file, ensure_ascii=False, indent=4)

print(f'Holidays data saved to {year}.json')
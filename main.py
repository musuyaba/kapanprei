import requests
from bs4 import BeautifulSoup
import json
import re
import os
from dotenv import load_dotenv
from maps import month_map 
from arguments import get_year
from loggers import setup_logging

def main():
    """
    Main function to scrape holiday data for a specified year and save it to monthly JSON files.
    Includes error handling and logging for various potential issues.
    """
    load_dotenv()
    
    log_directory = os.getenv('LOG_DIRECTORY', 'logging')
    storage_directory = os.getenv('STORAGE_DIRECTORY', 'storages')
    base_url = os.getenv('BASE_URL', 'https://tanggalan.com')

    logging = setup_logging(log_directory)
    logging.info("Script started")

    year = get_year()

    year_directory = f'{storage_directory}/{year}'
    os.makedirs(year_directory, exist_ok=True)

    url = f'{base_url}/{year}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f"Request to {url} successful")
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        logging.info("HTML content parsed successfully")
    except Exception as e:
        logging.error(f"Failed to parse HTML: {e}")
        return

    try:
        uls = soup.find_all('ul')
    except Exception as e:
        logging.error(f"Failed to find <ul> elements: {e}")
        return

    for ul in uls:
        try:
            first_li = ul.find_all('li')[0]
            month_year = first_li.find('a').get_text().strip()

            match = re.match(r'([a-zA-Z]+)(\d+)', month_year)
            if match:
                month_name = match.group(1).lower()
                extracted_year = match.group(2)

                month = month_map.get(month_name)
                if month is None:
                    logging.warning(f"Month '{month_name}' not found in month_map")
                    continue

                month_file_path = f'{year_directory}/{month}.json'
                if os.path.exists(month_file_path):
                    logging.info(f'File for {year}-{month} already exists. Skipping.')
                    continue

                holidays = []

                last_li = ul.find_all('li')[-1]
                tables = last_li.find_all('table')
        except Exception as e:
            logging.error(f"Failed to process <ul> element: {e}")
            continue

        for table in tables:
            try:
                trs = table.find_all('tr')
            except Exception as e:
                logging.error(f"Failed to find <tr> elements: {e}")
                continue

            for tr in trs:
                try:
                    tds = tr.find_all('td')
                    if len(tds) >= 2:
                        date = tds[0].get_text().strip()
                        holiday_name = tds[1].get_text().strip()

                        formatted_date = f'{extracted_year}-{month}-{date.zfill(2)}'

                        collective_leave = 'cuti' in holiday_name.lower()

                        holidays.append({
                            'date': formatted_date,
                            'holiday': holiday_name,
                            'collective_leave': collective_leave
                        })
                except Exception as e:
                    logging.error(f"Failed to process <tr> element: {e}")
                    continue

        try:
            with open(month_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(holidays, json_file, ensure_ascii=False, indent=4)
            logging.info(f'Holidays data for {year}-{month} saved to {month_file_path}')
        except Exception as e:
            logging.error(f"Failed to write JSON file: {e}")

    logging.info("Script finished")

if __name__ == "__main__":
    main()

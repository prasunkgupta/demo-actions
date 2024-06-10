import logging
import logging.handlers
import os

from bs4 import BeautifulSoup
    
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

url = 'https://city.imd.gov.in/citywx/city_weather.php?id=42111'

if __name__ == "__main__":
    r = requests.get(url=url)
    if r.status_code == 200:
        soup = BeautifulSoup(
            r.content,
            'html.parser'
        )
        table = soup.find('table')
        rows = table.find_all('tr')
        i = 0
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if i != 0 and i <= 12:
                logger.info(f"{' '.join(cols)}")
            i += 1
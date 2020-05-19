from bs4 import BeautifulSoup
from datetime import timedelta
import requests
import requests_cache
from time import sleep
from models import Detainee
from peewee import DoesNotExist
from lxml import html

requests_cache.install_cache(
    'cache',
    expire_after=timedelta(hours=24),
    allowable_methods=('GET', 'POST')
)

SEARCH_URL = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.I00030s'

def get_detainees():
  print("Getting detainee data.")
  headers = {'user-agent': 'my-app/0.0.1'}
  r = requests.get(SEARCH_URL, headers=headers)
  soup = BeautifulSoup(r.content, 'lxml')
  rows = soup.find(id='mrc_main_table').find_all('tr')
  count = 0

  for row in rows:
    cells = row.find_all('td')

    if(len(cells)>0):
      button_link = cells[9].find('a')
      href = button_link['href']
      details_url = "https://report.boonecountymo.org/mrcjava/servlet/" + href
      r = requests.get(details_url, headers=headers)
      soup = BeautifulSoup(r.content, 'lxml')
      count = count + 1
           mugshotDiv = soup.find(class_='mugshotDiv', attrs={"data-count": count})
      infoContainer = mugshotDiv.find(class_='infoContainer')
      info_cells = infoContainer.find_all('td')
      chargeContainer = mugshotDiv.find(class_='chargesContainer')
      charges_rows = chargeContainer.find_all('tr')
      charges_cells = charges_rows[1].find_all('td')
     
      extract_detainee_data(cells, info_cells, charges_cells)

      sleep(1)
  
def extract_detainee_data(cells, info_cells, charges_cells):
  print("Extracting detainee data.")

  Detainee.create(
    last_name = cells[0].text.strip(),
    first_name = cells[1].text.strip(),
    middle_name = cells[2].text.strip(),
    suffix = cells[3].text.strip(),
    sex = cells[4].text.strip(),
    race = cells[5].text.strip(),
    age = cells[6].text.strip(),
    city = cells[7].text.strip(),
    state = cells[8].text.strip(),

    height = info_cells[1].text.strip(),
    weight = info_cells[3].text.strip(),
    eyes = info_cells[7].text.strip(),
    hair = info_cells[9].text.strip(),

    case_number = charges_cells[0].text.strip(),
    charge_description = charges_cells[1].text.strip(),
    charge_status = charges_cells[2].text.strip(),
    bail_amount = charges_cells[3].text.strip(),
    bond_type = charges_cells[4].text.strip(),
    court_date = charges_cells[5].text.strip(),
    court_time = charges_cells[6].text.strip(),
    court_of_jurisdiction = charges_cells[7].text.strip(),
  )

def main():
    get_detainees()
    print("Done.")

if __name__ == '__main__':
    main()


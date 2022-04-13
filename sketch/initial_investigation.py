import requests
from bs4 import BeautifulSoup

BBC_URL = "https://www.bbc.com/news/world/us_and_canada"

response = requests.get(BBC_URL)
soup = BeautifulSoup(response)

# fmt: off
from IPython import embed; embed() # JTODO: remove
# fmt: on

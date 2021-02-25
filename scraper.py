import requests
from bs4 import BeautifulSoup

website = "https://www.rogueaustralia.com.au/monster-rhino-belt-squat-stand-alone-mg-black-au"
page = requests.get(website)
soup = BeautifulSoup(page.text, 'html.parser')
status = soup.find(class_='button btn-size-m gray full')
x = status.find(class_='block slot')
name = soup.find(class_='name')
print(name.contents)
print(x.contents)
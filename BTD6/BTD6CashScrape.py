import requests
from sys import exit as sys_ex
from sys import argv
from bs4 import BeautifulSoup as bs, ResultSet

baseURL = "https://bloons.fandom.com/wiki/"
std = "Rounds_(BTD6)"
alt = "Alternate_Bloons_Rounds"

args = argv[1:]

if ("-a" in args):
    mode = "alt"
    URL = baseURL + alt
else:
    URL = baseURL + std
    mode = "std"

# Connect
page = requests.get(URL)
if page.status_code == requests.codes.ok:
    print("Connection successful!")
    outFile = open("BTD6Money.csv", "wt", encoding="utf-8")
    outFile.write(f"Round,Money\n")
else:
    print("Error connecting to site")
    sys_ex

# Get Table
if mode == "alt":
    soup = bs(page.text, "lxml")
    tables = soup.find_all("table")
    table = tables[2]
    rows = table.find_all("tr")
    i = 2
    while i < 102:
        temp = rows[i].find_all("td")
        outFile.write(f"{i-1},{temp[4].text}")
        i += 1

else:
    soup = bs(page.text, "lxml")
    table = soup.find("table")
    rows = table.find_all("tr")
    i = 2
    while i < 142:
        temp = rows[i].find_all("td")
        outFile.write(f"{i-1},{temp[4].text}")
        i += 1

outFile.close()

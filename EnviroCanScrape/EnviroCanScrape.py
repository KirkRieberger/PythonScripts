import requests
import re
import time
from bs4 import BeautifulSoup as bs

#TODO: Province Select. Cmd line arg?

stats = open('performanceStats.txt', 'w')

start = time.perf_counter()

num = 1 # Cities start at 1 (Cochrane)
cities = {}
reqTotal = 0
parseTotal = 0
regTotal = 0

while num < 73: # City number 72 (Edson) is last
    if num % 5 == 0:
        #TODO: Replace with progress bar https://builtin.com/software-engineering-perspectives/python-progress-bar
        print(f'City number {num}...')
    stats.write(f'City #{num}:\n---------\n')
    reqStart = time.perf_counter()
    url = f'https://weather.gc.ca/city/pages/ab-{num}_metric_e.html'
    page = requests.get(url)
    if page.status_code != requests.codes.ok:
        print(f'Error on city number {num}!\nContinuing...')
        num += 1
        reqEnd = time.perf_counter()
        reqTime = reqEnd - reqStart
        stats.write(f'Request: {reqTime:18}s, Parse: 0.s, Regex: 0s\n\n')
        continue
    
    reqEnd = time.perf_counter()

    parseStart = time.perf_counter()
    soup = bs(page.text, 'lxml')
    name = soup.find('h1', {'property' : 'name'}).get_text()
    parseEnd = time.perf_counter()

    regStart = time.perf_counter()
    name = re.sub('(, AB)', '', name)
    cities.update([(num, name)])
    regEnd = time.perf_counter()
    
    reqTime = reqEnd - reqStart
    parseTime = parseEnd - parseStart
    regTime = regEnd - regStart

    reqTotal += reqTime
    parseTotal += parseTime
    regTotal += regTime
    stats.write(f'Request: {reqTime:18}s, Parse: {parseTime:20}s, Regex: {regTime:21}s\n\n')
    num += 1

stats.write('Average:\n---------\n')
stats.write(f'Request: {reqTotal/(num-1):18}s, Parse: {parseTotal/(num-1):20}s, Regex: {regTotal/(num-1)}s')

with open('EnviroCanCities.csv', 'w') as outCSV:
    outCSV.write('Index,Locale\n')
    for key, value in cities.items():
        outCSV.write(f'{key},{value}\n')

end = time.perf_counter()
elapsed = round(end - start, 2)
print(f'\nElapsed time: {elapsed}s')
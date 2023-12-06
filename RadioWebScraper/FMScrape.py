# FMScrape.py - A small web scraper to find radio stations in Alberta, Canada.
# Copyright (C) 2023 Kirk Rieberger
# Issued under GPLv2 or later
# See LICENCE.txt for full license

#TODO: Command line args to select province, AM/FM/Both

import requests
import re
import time
import sys
from bs4 import BeautifulSoup as bs

class DataSources:
    bc = 'https://www.canadianradiodirectory.com/british-columbia/'
    ab = 'https://www.canadianradiodirectory.com/alberta/'
    sk = 'https://www.canadianradiodirectory.com/saskatchewan/'
    mb = 'https://www.canadianradiodirectory.com/manitoba/'
    on = 'https://www.canadianradiodirectory.com/ontario/'
    qc = 'https://www.canadianradiodirectory.com/quebec/'
    nb = 'https://www.canadianradiodirectory.com/new-brunswick/'
    ns = 'https://www.canadianradiodirectory.com/nova-scotia/'
    pe = 'https://www.canadianradiodirectory.com/prince-edward-island/'
    nl = 'https://www.canadianradiodirectory.com/newfoundland-labrador/'
    yt = 'https://www.canadianradiodirectory.com/yukon/'
    nt = 'https://www.canadianradiodirectory.com/northwest-territories/'
    nu = 'https://www.canadianradiodirectory.com/nunavut/'

sources = DataSources()

start = time.perf_counter()

url = sources.alberta

page = requests.get(url)
print('Requesting data from Alberta radio directory...')
if page.status_code == requests.codes.ok:
    print('Connection successful!')
else:
    print('Error connecting to site')
    sys.exit(1)

soup = bs(page.text, 'lxml')

table = soup.find('table')
rows = table.find_all('tr')

# Row 0 is spacing
# Row 1 is site heading and date
# Row 2 is spacing
# Row 3 is column labels
# Row 4 and beyond are radio station data

file = open('AltaRadioStations.txt', 'w', encoding='UTF-8')

date = str(rows[1].find_all('td')[3])
# Regex to strip HTML tags from the date
date = re.sub('<[^<]+?>', '', date)

file.write('Date Updated: ' + date + '\n\n')

i = 4
while (i < len(list(rows))):
    # Parse table data (td) fields, skipping programming format, station name,
    # and station call sign, one row at a time
    temp = rows[i].find_all('td')
    out = []
    j = 0
    while (j < 8):
        # Skip programming format, station name, and call sign
        if j == 3 or j == 4 or j == 5:
            j += 1
            continue
        out.append(temp[j].text)
        j += 1
    # Exit at first spacing line after data lines
    if out == ['', '', '', '', '']:
        break
    # Don't care about AM stations
    elif out[2] == 'AM' or out[2] == 'HD1' or out[2] == 'HD2':
        i += 1
        continue
    # Convert to standard power units
    elif out[4] == 'kW':
        out[3] = int(float(out[3])*1000)
        out[4] = 'w'
    k = 0
    while k < 5:
        if k == 2:
            k += 1
            continue
        file.write('%s%s' % (out[k], ' '))  # f string
        k += 1
    file.write('\n')
    i += 1

file.close()

end = time.perf_counter()
elapsed = round(end - start, 2)
print(f'\nElapsed time: {elapsed}s')

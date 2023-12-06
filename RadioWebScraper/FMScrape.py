# FMScrape.py - A small web scraper to find radio stations in Alberta, Canada.
# Copyright (C) 2023 Kirk Rieberger
# Issued under GPLv2 or later
# See LICENCE.txt for full license

#TODO: Command line args to select province, AM/FM/Both
#TODO: Command line args to select columns (Location, Frequency, Band, Station Name, Format, Call Sign, Power)
import requests
import time
import sys
from bs4 import BeautifulSoup as bs

class DataSources:
    bc_url = 'https://www.canadianradiodirectory.com/british-columbia/'
    bc = 'BC'
    ab_url = 'https://www.canadianradiodirectory.com/alberta/'
    ab = 'Alberta'
    sk_url = 'https://www.canadianradiodirectory.com/saskatchewan/'
    sk = 'Saskatchewan'
    mb_url = 'https://www.canadianradiodirectory.com/manitoba/'
    mb = 'Manitoba'
    on_url = 'https://www.canadianradiodirectory.com/ontario/'
    on = 'Ontario'
    qc_url = 'https://www.canadianradiodirectory.com/quebec/'
    qc = 'Quebec'
    nb_url = 'https://www.canadianradiodirectory.com/new-brunswick/'
    nb = 'NewBrunswick'
    ns_url = 'https://www.canadianradiodirectory.com/nova-scotia/'
    ns = 'NovaScotia'
    pe_url = 'https://www.canadianradiodirectory.com/prince-edward-island/'
    pe = 'PEI'
    nl_url = 'https://www.canadianradiodirectory.com/newfoundland-labrador/'
    nl = 'Newfoundland-Labrador'
    yt_url = 'https://www.canadianradiodirectory.com/yukon/'
    yt = 'Yukon'
    nt_url = 'https://www.canadianradiodirectory.com/northwest-territories/'
    nt = 'NorthwestTerritories'
    nu_url = 'https://www.canadianradiodirectory.com/nunavut/'
    nu = 'Nunavut'

    
sources = DataSources()


def getData(url, prov):
    page = requests.get(url)
    print(f'Requesting data from {prov} radio directory...')
    if page.status_code == requests.codes.ok:
        print('Connection successful!')
    else:
        print('Error connecting to site')
        sys.exit(1)

    soup = bs(page.text, 'lxml')

    table = soup.find('table')
    rows = table.find_all('tr')

    return rows

def parseData(rows):

    # Row 0 is spacing
    # Row 1 is province/territory heading and date
    # Row 2 is spacing
    # Row 3 is column labels
    # Row 4 and beyond are radio station data

    # file = open(f'{prov}RadioStations.txt', 'w', encoding='UTF-8')

    outputBuffer = ""

    date = str(rows[1].find_all('td')[3].text)
    outputBuffer += f'Date Updated: {date}\n\n'

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
            outputBuffer += f'{out[k] }' #('%s%s' % (out[k], ' '))  # f string
            k += 1
        outputBuffer += '\n'
        i += 1

    return outputBuffer
    # file.close()


def main():
    rows = getData(sources.ab_url, sources.ab)
    data = parseData(rows)
    print("Nominal print to stop debugger")


if __name__ == "__main__":
    main()
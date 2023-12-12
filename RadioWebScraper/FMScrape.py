# FMScrape.py - A small web scraper to find radio stations in Alberta, Canada.
# Copyright (C) 2023 Kirk Rieberger
# Issued under GPLv2 or later
# See LICENCE.txt for full license

# TODO: Command line args to select province, AM/FM/Both
# TODO: Command line args to select columns (Location, Frequency, Band, Station Name, Format, Call Sign, Power)
# TODO: File type selector
import requests
import argparse
import time
import sys
from bs4 import BeautifulSoup as bs

baseURL = "https://www.canadianradiodirectory.com"
dataSources = {
    "BC": f"{baseURL}/british-columbia/",
    "AB": f"{baseURL}/alberta/",
    "SK": f"{baseURL}/saskatchewan/",
    "MB": f"{baseURL}/manitoba/",
    "ON": f"{baseURL}/ontario/",
    "QC": f"{baseURL}/quebec/",
    "NB": f"{baseURL}/new-brunswick/",
    "NS": f"{baseURL}/nova-scotia/",
    "PE": f"{baseURL}/prince-edward-island/",
    "NL": f"{baseURL}/newfoundland-labrador/",
    "YT": f"{baseURL}/yukon/",
    "NT": f"{baseURL}/northwest-territories/",
    "NU": f"{baseURL}/nunavut/",
}


def getData(url, prov):
    print(f"Requesting data from {prov} radio directory...")
    page = requests.get(url)
    if page.status_code == requests.codes.ok:
        print("Connection successful!")
    else:
        print("Error connecting to site")
        sys.exit(1)

    soup = bs(page.text, "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")

    return rows


def parseData(rows):
    # Row 0 is spacing
    # Row 1 is province/territory heading and date
    # Row 2 is spacing
    # Row 3 is column labels
    # Row 4 and beyond are radio station data

    # file = open(f'{prov}RadioStations.txt', 'w', encoding='UTF-8')

    outputBuffer = ""

    date = str(rows[1].find_all("td")[3].text)
    outputBuffer += f"Date Updated: {date}\n\n"

    i = 4
    while i < len(list(rows)):
        # Parse table data (td) fields, skipping programming format, station name,
        # and station call sign, one row at a time
        temp = rows[i].find_all("td")
        out = []
        j = 0
        while j < 8:
            # Skip programming format, station name, and call sign
            if j == 3 or j == 4 or j == 5:
                j += 1
                continue
            out.append(temp[j].text)
            j += 1
        # Exit at first spacing line after data lines
        if out == ["", "", "", "", ""]:
            break
        # Don't care about AM stations
        elif out[2] == "AM" or out[2] == "HD1" or out[2] == "HD2":
            i += 1
            continue
        # Convert to standard power units
        elif out[4] == "kW":
            out[3] = int(float(out[3]) * 1000)
            out[4] = "w"
        k = 0
        while k < 5:
            if k == 2:
                k += 1
                continue
            outputBuffer += f"{out[k]} "  # ('%s%s' % (out[k], ' '))  # f string
            k += 1
        outputBuffer += "\n"
        i += 1

    return outputBuffer
    # file.close()


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-bc", "--BritishColumbia", action="store_true", help="")
    parser.add_argument("-ab", "--Alberta", action="store_true", help="")
    parser.add_argument("-sk", "--Saskatchewan", action="store_true", help="")
    parser.add_argument("-mb", "--Manitoba", action="store_true", help="")
    parser.add_argument("-on", "--Ontario", action="store_true", help="")
    parser.add_argument("-qc", "--Quebec", action="store_true", help="")
    parser.add_argument("-nb", "--NewBrunswick", action="store_true", help="")
    parser.add_argument("-ns", "--NovaScotia", action="store_true", help="")
    parser.add_argument("-pe", "--PEI", action="store_true", help="")
    parser.add_argument("-nl", "--Newfoundland", action="store_true", help="")
    parser.add_argument("-yt", "--Yukon", action="store_true", help="")
    parser.add_argument("-nt", "--NorthwestTerritories", action="store_true", help="")
    parser.add_argument("-nu", "--Nunavut", action="store_true", help="")
    parser.add_argument(
        "-all",
        "--All",
        action="store_true",
        help="Get radio data for all provinces. This argument supercedes all others",
    )
    parser.add_argument("-prov", "--Province", help="")

    argsNamespace = parser.parse_args()

    if argsNamespace.All:
        for prov in dataSources:
            rows = getData(dataSources.get(prov), prov)
            data = parseData(rows)
            outFile = open("CanadaRadioDirectory.txt", "wt")
            outFile.write(data + "\n")
            print(f"Processed {prov}")

    toGet = []
    args = vars(argsNamespace)
    for arg in args:
        if args.get(arg):
            toGet.append(arg)

    rows = getData(dataSources.keys(), dataSources.values())
    data = parseData(rows)


if __name__ == "__main__":
    main()

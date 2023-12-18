# FMScrape.py - A small web scraper to find radio stations in Alberta, Canada.
# Copyright (C) 2023 Kirk Rieberger
# Issued under GPLv2 or later
# See LICENCE.txt for full license

# TODO: Command line args to select province, AM/FM/Both
# TODO: Command line args to select columns (Location, Frequency, Band, Station Name, Format, Call Sign, Power)
# TODO: File type selector
import requests
import argparse

# import time
from sys import exit as sys_ex
from bs4 import BeautifulSoup as bs, ResultSet

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


def nameToAbbr(longName: str):
    """Converts the long province name from the Argument Parser to the ISO 3166-2:CA provincial abbreviation

    Args:
        longName (str): The long-form province name

    Returns:
        str: The ISO standard province name abbreviation
    """
    match longName:
        case "BritishColumbia":
            return "BC"
        case "Alberta":
            return "AB"
        case "Saskatchewan":
            return "SK"
        case "Manitoba":
            return "MB"
        case "Ontario":
            return "ON"
        case "Quebec":
            return "QC"
        case "NewBrunswick":
            return "NB"
        case "NovaScotia":
            return "NS"
        case "PEI":
            return "PE"
        case "Newfoundland":
            return "NL"
        case "Yukon":
            return "YT"
        case "NorthwestTerritories":
            return "NT"
        case "Nunavut":
            return "NU"


def getData(prov: str, url: str):
    """Connects to the Canadian Radio Directory to get a current list of radio stations in a province

    Args:
        prov (str): The short name of the desired province
        url (str): The destination URL for the desired province

    Returns:
        ResultSet: The HTML table the data is stored in split into rows
    """
    print(f"Requesting data from {prov} radio directory...")
    page = requests.get(url)
    if page.status_code == requests.codes.ok:
        print("Connection successful!")
    else:
        print("Error connecting to site")
        sys_ex

    soup = bs(page.text, "lxml")

    table = soup.find("table")
    rows = table.find_all("tr")

    return rows


def parseData(rows: ResultSet):
    """Parses the incoming ResultSet into human-useable data

    Args:
        rows (ResultSet): A set of <tr> elements in a ResultSet container

    Returns:
        str: An output buffer ready to be written to disk
    """
    # Row 0 is spacing
    # Row 1 is province/territory heading and update date
    # Row 2 is spacing
    # Row 3 is column labels
    # Row 4 and beyond are radio station data
    # Columns: [Location, Frequency, Band, Name, Format, Call Sign, Power, Units]

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


def createParser():
    """Create an instance of argparse with all the required arguments

    Returns:
        ArgumentParser: The finished Argument Parser
    """
    parser = argparse.ArgumentParser(
        description="", usage="%(prog)s -prov <province(s)> or -<province(s)> or -all"
    )
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
        "-a",
        "--All",
        action="store_true",
        help="Get radio data for all provinces. This argument supercedes all others",
    )
    parser.add_argument(
        "-p",
        "--Province",
        choices=list(dataSources.keys()),
        type=str.upper,
        nargs="*",
        metavar=" ".join(dataSources.keys()),
        help="",
    )

    return parser


def checkAll(argsNamespace: argparse.Namespace):
    """Check for "all" argument on its own and in Province list (if non-empty)

    Args:
        argsNamespace (argparse.Namespace): The parsed arguments

    Returns:
        bool: If the "all" flag is set anywhere in the arguments
    """
    if argsNamespace.All:
        return True
    elif argsNamespace.Province is not None:
        if "all" in map(str.lower, argsNamespace.Province):
            return True
        else:
            return False
    else:
        return False


def processAll():
    """
    Processes all provinces and territories
    """
    outFile = open("CanadaRadioDirectory.txt", "wt", encoding="UTF-8")
    outFile.close()
    for prov in dataSources:
        rows = getData(prov, dataSources.get(prov))
        data = parseData(rows)
        outFile = open("CanadaRadioDirectory.txt", "at", encoding="UTF-8")
        outFile.write(data + "\n")
        print(f"Processed {prov}")
        outFile.close()
    sys_ex()


def main():
    parser = createParser()
    argsNamespace = parser.parse_args()

    all = checkAll(argsNamespace)

    # Process all provinces if all option selected
    if all:
        processAll()

    # Determine which provinces need to be processed
    args = vars(argsNamespace)
    if args.get("Province") is None:
        toProcess = []
        # Check other args
        for arg in args:
            if args.get(arg):
                toProcess.append(nameToAbbr(arg))  # use for progress bar
    else:
        toProcess = args.get("Province")

    # Process provinces
    for prov in toProcess:
        rows = getData(prov, dataSources.get(prov))
        data = parseData(rows)
        outFile = open(f"{prov}RadioDirectory.txt", "wt", encoding="UTF-8")
        outFile.write(data)
        outFile.close()


if __name__ == "__main__":
    main()

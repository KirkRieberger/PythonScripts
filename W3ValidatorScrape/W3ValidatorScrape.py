import argparse
import requests
import os
from datetime import datetime
from sys import exit as sys_ex
from bs4 import BeautifulSoup as bs  # Also requires lxml to be installed
from progress.bar import Bar


def validateHTML(inFile):
    """
    Upload a file to the W3 Consortium HTML Validator and return a list of errors.
    ### Params:
        inFile : An OS Encoded Filename in the current working directory

    ### Returns:
        outStr : A string of warnings and errors
    """
    url = "https://validator.w3.org/nu/#file"
    # Upload file to be tested
    file = open(inFile, "rb")
    page = requests.post(url, data={"s": "Upload"}, files={"file": file})
    # Parse returned page
    soup = bs(page.text, "lxml")
    list = soup.find("ol")

    try:
        errors = list.find_all("li")
    except AttributeError:  # If no unordered list
        return "✔"  # Unicode 0x2714

    outStr = ""

    for element in errors:
        if element.find("span", {"class": "first-line"}) is not None:
            row = element.find("span", {"class": "first-line"}).text
        elif element.find("span", {"class": "last-line"}) is not None:
            row = element.find("span", {"class": "last-line"}).text
        else:
            row = "None"

        if "warning" in element.attrs["class"]:
            if row != "None":
                outStr += f"Line {row} - {element.find('p').text}\n"
            else:
                outStr += f"{element.find('p').text}\n"
        elif "error" in element.attrs["class"]:
            if row != "None":
                outStr += f"Line {row} - {element.find('p').text}\n"
            else:
                outStr += f"{element.find('p').text}\n"

    if len(outStr) == 0:
        return "✔"  # Unicode 0x2714
    else:
        return outStr


def validateCSS(inFile):
    """
    Upload a file to the W3 Consortium CSS Validator and return a list of errors.
    ### Params:
        inFile : An OS Encoded Filename in the current working directory

    ### Returns:
        outStr : A string of warnings and errors
    """
    url = "https://jigsaw.w3.org/css-validator/validator"
    # Upload file to be tested
    file = open(inFile, "rb")
    page = requests.post(url, data={"text": file})
    if page.status_code != requests.codes.ok:
        now = datetime.now()
        timeStr = f"{now.date()}-T{now.hour}-{now.minute}"
        logOut = open(f"validator-{timeStr}.log", "wt")
        logOut.write(page.text)
        logOut.close()
        return "Request Error. See log"

    # Parse returned page
    soup = bs(page.text, "lxml")
    list = soup.find("tbody")

    try:
        errors = list.find_all("tr")
    except AttributeError:  # If no unordered list
        return "✔"  # Unicode 0x2714

    outStr = ""

    for line in errors:
        if line.find("td", {"class": "linenumber"}) is not None:
            row = line.find("span", {"class": "linenumber"}).text
        elif line.find("span", {"class": "last-line"}) is not None:
            row = line.find("span", {"class": "last-line"}).text
        else:
            row = "None"

        outStr += f"Line {row}"

    if len(outStr) == 0:
        return "✔"  # Unicode 0x2714
    else:
        return outStr


def main():
    parser = argparse.ArgumentParser(
        description="Submit all HTML files in a directory to the W3 Consortium HTML Validator."
    )
    parser.add_argument(
        "dir", type=str, help="The directory of Webpage source files to be validated"
    )
    parser.add_argument("-v", "--HTML", action="store_true", help="Validate HTML files")
    parser.add_argument("-c", "--CSS", action="store_true", help="Validate CSS files")
    args = parser.parse_args()

    dir = os.fsencode(args.dir)
    if not os.path.isdir(dir):
        print("Error: Directory specified does not exist!\n")
        sys_ex()

    os.chdir(dir)

    outFile = open("testOut.txt", "w", encoding="UTF-8")

    if args.HTML:
        htmlList = {}
        for file in os.listdir(dir):  # file == bytes
            filename = os.fsdecode(file)  # String
            if filename.lower().endswith(".html") or filename.lower().endswith(".htm"):
                htmlList.update({filename: file})

        progBar = Bar("Validating HTML", max=len(htmlList))
        for key in htmlList.keys():
            outFile.write(f"{os.fsdecode(htmlList.get(key))}:\n")
            outFile.write(f"{validateHTML(htmlList.get(key))}\n")
            progBar.next()

    if args.CSS:
        cssList = {}
        for file in os.listdir(dir):  # file == bytes
            filename = os.fsdecode(file)  # String
            if filename.endswith(".css"):
                cssList.update({filename: file})

        progBar = Bar("Validating CSS", max=len(cssList))
        for key in cssList.keys():
            outFile.write(f"{os.fsdecode(cssList.get(key))}:\n")
            outFile.write(f"{validateCSS(cssList.get(key))}")
            progBar.next()

    outFile.close()


if __name__ == "__main__":
    main()

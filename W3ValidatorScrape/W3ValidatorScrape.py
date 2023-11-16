import argparse
import requests
import os
from sys import exit as sys_ex
from bs4 import BeautifulSoup as bs


def testFile(inFile):
    '''
    Upload a file to the W3 Consortium HTML Validator and return a list of errors.
    ### Params:
    inFile : An OS Encoded Filename in the current working directory

    ### Returns:
        outStr : A string of warnings and errors
    '''
    url = 'https://validator.w3.org/nu/#file'
    # Upload file to be tested
    file = open(inFile, 'rb')
    page = requests.post(url, data={'s': 'Upload'}, files={'file': file})
    # Parse returned page
    soup = bs(page.text, 'lxml')
    list = soup.find('ol')

    try:
        errors = list.find_all('li')
    except AttributeError:
        return "✔"  # Unicode 0x2714

    outStr = ""

    for element in errors:
        if element.find("span", {"class": "first-line"}) is not None:
            row = element.find("span", {"class": "first-line"}).text
        elif element.find("span", {"class": "last-line"}) is not None:
            row = element.find("span", {"class": "last-line"}).text
        else:
            row = "None"

        if "warning" in element.attrs['class']:
            if row != "None":
                outStr += f"Line {row} - {element.find('p').text}\n"
            else:
                outStr += f"{element.find('p').text}\n"
        elif "error" in element.attrs['class']:
            if row != "None":
                outStr += f"Line {row} - {element.find('p').text}\n"
            else:
                outStr += f"{element.find('p').text}\n"

    return outStr


def main():
    parser = argparse.ArgumentParser(
        description="Submit all HTML files in a directory to the W3 Consortium HTML Validator.")
    parser.add_argument('dir', type=str,
                        help="The directory of HTML files to be validated")
    # parser.add_argument()
    args = parser.parse_args()

    dir = os.fsencode(args.dir)
    if (not os.path.isdir(dir)):
        print("Error: Directory specified does not exist!\n")
        sys_ex()

    os.chdir(dir)

    outFile = open("testOut.txt", "w", encoding="UTF-8")

    fileList = {}
    for file in os.listdir(dir):  # file == bytes
        filename = os.fsdecode(file)  # String
        if filename.endswith(".html") or filename.endswith(".htm"):
            fileList.update({filename: file})

    for key in fileList.keys():
        print(f"Processing {key}...")
        outFile.write(f"{fileList.get(key)}:\n")
        outFile.write(f"{testFile(fileList.get(key))}\n")

    outFile.close()


if __name__ == "__main__":
    main()

# resistor.py - A simple through-hole resistor colour band decoder.
# Copyright (C) 2023 Kirk Rieberger
# Issued under GPLv2 or later
# See LICENCE.txt for full license

import sys
from pathlib import Path

# From: https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
# Get the utils module from up the directory tree
if __name__ == "__main__":
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[2]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))

    except ValueError:
        pass

    __package__ = 'PythonScripts.ResistorColourCode'

from .. import utils

# TODO: Error/input checking
# TODO: Regex character decoding (BrBlBrGld -> 100 5%)

debugMode = True
# TODO: 6 band - temp coeff
digitBand = {'black': '0', 'brown': '1', 'red': '2', 'orange': '3',
             'yellow': '4', 'green': '5', 'blue': '6', 'violet': '7',
             'grey': '8', 'white': '9', 'gold': '-1', 'silver': '-1', '': ''}

multiplyBand = {'black': 1, 'brown': 10, 'red': 100, 'orange': 1000,
                'yellow': 1e4, 'green': 1e5, 'blue': 1e6, 'violet': 1e7,
                'grey': 1e8, 'white': 1e9, 'gold': 0.1, 'silver': 0.01}

toleranceBand = {'black': -1, 'brown': 1, 'red': 2, 'orange': -1, 'yellow': -1,
                 'green': 0.5, 'blue': 0.25, 'violet': 0.1, 'grey': 0.05,
                 'white': -1, 'gold': 5, 'silver': 10}


def checkValidColour(inputVector, inputLength):
    inputPos4 = ['First Band', 'Second Band',
                 'sig3', 'Third Band', 'Fourth Band']
    inputPos5 = ['First Band', 'Second Band',
                 'Third Band', 'Fourth Band', 'Fifth Band']
    valid = True
    if len(inputVector) != 5:
        utils.printErr("Invalid input size!")
        return False
    i = 0
    while i < 5:
        if inputVector[i] in digitBand.keys():
            pass
        else:
            valid = False
            match inputLength:
                case 4:
                    print(f'Error in {inputPos4[i]}!')
                case 5:
                    print(f'Error in {inputPos5[i]}!')
                case _:
                    utils.printErr(f'Input length error!')

        i += 1

    return (valid)


def main():
    inputVector = [-1, -1, -1, -1, -1]

    while True:
        try:
            numBands = int(input("How many bands? (4 or 5): "))
        except ValueError:
            print('Please enter a valid input (4 or 5)!')
            continue
        match numBands:
            case 4:
                inputVector[0] = input('First band colour: ').lower()
                inputVector[1] = input('Second band colour: ').lower()
                inputVector[2] = ''
                inputVector[3] = input('Third band colour: ').lower()
                inputVector[4] = input('Fourth band colour: ').lower()
            case 5:
                inputVector[0] = input('First band colour: ').lower()
                inputVector[1] = input('Second band colour: ').lower()
                inputVector[2] = input('Third band colour: ').lower()
                inputVector[3] = input('Fourth band colour: ').lower()
                inputVector[4] = input('Fifth band colour: ').lower()
            case _:
                print('Please enter a valid input (4 or 5)!')
                continue

        valid = checkValidColour(inputVector, numBands)

        if not valid:
            continue

        value = int(digitBand.get(inputVector[0]) + digitBand.get(inputVector[1]) +
                    digitBand.get(inputVector[2]))*multiplyBand.get(inputVector[3])
        print(
            f'Resistor value: {value} ± {toleranceBand.get(inputVector[4])}%')

        while True:
            cont = input('Continue?(y/n): ')
            match cont:
                case 'y':
                    break
                case 'n':
                    exit(0)
                case _:
                    print('Please enter a valid input (y/n)!')
                    continue


if __name__ == "__main__":
    main()

# Command Line Resistor Decoder
# Author - Kirk Rieberger
# Version - 0.1

import utils
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


def main():
    while True:
        numBands = input("How many bands? (4 or 5): ")

        match numBands:
            case '4':
                sig1 = input('First band colour: ')
                sig2 = input('Second band colour: ')
                sig3 = ''
                mult = input('Third band colour: ')
                tol = input('Fourth band colour: ')
            case '5':
                sig1 = input('First band colour: ')
                sig2 = input('Second band colour: ')
                sig3 = input('Third band colour: ')
                mult = input('Fourth band colour: ')
                tol = input('Fifth band colour: ')
            case _:
                print('Please enter a valid input (4 or 5)!')
                continue

        value = int(digitBand.get(sig1) + digitBand.get(sig2) +
                    digitBand.get(sig3))*multiplyBand.get(mult)
        print(f'Resistor value: {value} ± {toleranceBand.get(tol)}%')


if __name__ == "__main__":
    main()

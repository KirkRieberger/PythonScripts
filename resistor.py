# Command Line Resistor Decoder
# Author - Kirk Rieberger
# Version - 0.1

import utils

debugMode = True

digitBand = {'black': 0, 'brown': 1, 'red': 2, 'orange': 3, 'yellow': 4,
             'green': 5, 'blue': 6, 'violet': 7, 'grey': 8, 'white': 9,
             'gold': -1, 'silver': -1}

multiplyBand = {'black': 1, 'brown': 10, 'red': 100, 'orange': 1000,
                'yellow': 1e4, 'green': 1e5, 'blue': 1e6, 'violet': 1e7,
                'grey': 1e8, 'white': 1e9, 'gold': 0.1, 'silver': 0.01}

toleranceBand = {'black': -1, 'brown': 1, 'red': 2, 'orange': -1, 'yellow': -1,
                'green': 0.5, 'blue': 0.25, 'violet': 0.1, 'grey': 0.05,
                'white': -1, 'gold': 5, 'silver': 10}

def main():
    pass


if __name__ == "__main__":
    main()
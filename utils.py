# utils.py - A small header to define coloured print statements
# Copyright (C) 2023 Kirk Rieberger
# Issued under GPLv2 or later
# See LICENCE.txt for full license

class bcolours:
    HEADER = '\033[95m'  # Magenta
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'  # Yellow
    FAIL = '\033[91m'  # Red
    ENDC = '\033[0m'  # Default
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


debugMode = False  # Default value so linter doesn't complain


def printWarn(inStr, lineEnd='\n'):
    """
    [Debug] Prints the input string to the terminal in yellow.

    Parameters:
        inStr -- The thing to be printed
    """
    global debugMode
    if debugMode:
        print(bcolours.WARNING + str(inStr) + bcolours.ENDC, end=lineEnd)


def printErr(inStr, lineEnd='\n'):
    """
    [Debug] Prints the input string to the terminal in red.

    Keyword Argument:
    inStr -- The thing to be printed
    """
    global debugMode
    if debugMode:
        print(bcolours.FAIL + str(inStr) + bcolours.ENDC, end=lineEnd)


def printHeader(inStr, lineEnd='\n'):
    """
    Prints the input string to the terminal in magenta.

    Keyword Argument:
    inStr -- The thing to be printed
    """

    print(bcolours.HEADER + str(inStr) + bcolours.ENDC, end=lineEnd)


def printCyan(inStr, lineEnd='\n'):
    """
    Prints the input string to the terminal in red.

    Keyword Argument:
    inStr -- The thing to be printed
    """

    print(bcolours.OKCYAN + str(inStr) + bcolours.ENDC, end=lineEnd)

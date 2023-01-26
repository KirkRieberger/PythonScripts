import TimeCalcGlobals as g


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


debugMode = False  # Default value so parser doesn't complain


def printWarn(inStr):
    """
    [Debug] Prints the input string to the terminal in yellow.

    Parameters:
        inStr -- The thing to be printed
    """
    global debugMode
    if debugMode:
        print(bcolours.WARNING + str(inStr) + bcolours.ENDC)


def printErr(inStr):
    """
    [Debug] Prints the input string to the terminal in red.

    Keyword Argument:
    inStr -- The thing to be printed
    """
    global debugMode
    if debugMode:
        print(bcolours.FAIL + str(inStr) + bcolours.ENDC)

import re
import TimeCalcGlobals as g
import utils
from configparser import ConfigParser
from math import floor


def welcome():
    """Prints the program's welcome message to the terminal"""

    print(utils.bcolours.HEADER + "Time adder V1.1" + utils.bcolours.OKCYAN +
          "\nPress enter with a blank time to calculate.\n" +
          f"Maximum number of times is {g.numIter}." + utils.bcolours.ENDC)


def stringDelimit():
    """
    Tokenizes input from command line into second, minute, and hour lists.
    If the input is empty, returns lists

    Parameters:
        none

    Returns:
        hours   -- integer list of parsed hours\n
        minutes -- integer list of parsed minutes\n
        seconds -- integer list of parsed second
    """
    hours: list[int] = []
    minutes: list[int] = []
    seconds: list[int] = []

    # Regex to tokenize input time
    pattern = re.compile(r"(\d+:+)")  # Matches xx:xx:xx:xx:......

    # Read in times to be operated on
    i = 1
    cont = 0
    while (i <= g.numIter):
        time = input("Time #" + str(i) + ": ")
        if time.lower() == 'exit':
            exit()
        # If the input is the blank string, go to the calculation
        elif time == '':
            cont = 1

        split = re.split(r'(\d+:+)', time)
        utils.printErr(split)

        j = 0
        while j < len(split):
            split[j] = split[j].replace(':', '')
            # If we find a token that isn't a number or the empty string added
            #   by the regex split, the input is invalid
            if not (split[j].isnumeric() or split[j] == ''):
                split = []
                break
            # Remove empty strings added by regex split
            if split[j] == '':
                split.remove(split[j])
            else:
                split[j] = int(split[j])
                j += 1
        if cont == 1:
            return (seconds, minutes, hours)
        else:
            # Append tokenized times to appropriate list(s)
            match len(split):
                case 1:  # Only Seconds
                    seconds.append(split[0])
                case 2:  # Minutes:Seconds
                    minutes.append(split[0])
                    seconds.append(split[1])
                case 3:  # Hours:Minutes:Seconds
                    hours.append(split[0])
                    minutes.append(split[1])
                    seconds.append(split[2])
                case _:  # Invalid time
                    print("Please enter a valid time")
                    continue
        i += 1
        if i > g.numIter:
            return (seconds, minutes, hours)

    print()


def addTime(seconds: list[int], minutes: list[int], hours: list[int]):
    """
    Adds lists of hours, minutes, and seconds using usual time rules and carry

    Parameters:
        seconds -- a list of integer seconds to be added\n
        minutes -- a list of integer minutes to be added\n
        hours   -- a list of integer hours to be added

    Returns:
        nothing: prints output to terminal, then exits the program
    """
    carryIn, outSec = addMinuteSecond(seconds)
    minutes.append(carryIn)

    carryIn, outMin = addMinuteSecond(minutes)
    hours.append(carryIn)

    outHour = sum(hours)

    # Format so printed answer looks like expected
    outSec = lengthPrepend(outSec, 1)

    outMin = lengthPrepend(outMin, 1)

    outHour = lengthPrepend(outHour, 1)

    print(f'Calculated time: {outHour}:{outMin}:{outSec}', end='\n\n')
    exit()


def addMinuteSecond(timeList: list[int]):
    """
    Sums a list of numbers capping the output at 60

    Parameters:
        timeList -- The list of numbers to be summed

    Returns:
        outTime  -- The calculated minutes/seconds\n
        carry    -- The number of times the sum exceeded 60
    """
    if len(timeList) < 1:
        return (0, 0)
    carry = 0
    outTime = 0
    for time in timeList:
        outTime += time
    if outTime > 60:
        carry = floor(outTime / 60)
        outTime -= 60*carry
    # print(f'calculated: {outTime}, Carry out: {carry}')
    return (carry, outTime)


def lengthPrepend(input, length, char='0'):
    if len(str(input)) <= length:
        input = char + str(input)
    return input


def readConfig():
    config_object = ConfigParser()
    config_object.read("TimeCalc.ini")

    runtimeInfo = config_object["RUNTIME_INFO"]
    g.numIter = int(runtimeInfo["numiter"])
    utils.debugMode = runtimeInfo["debugmode"] == 'True'


if __name__ == "__main__":
    readConfig()
    welcome()
    second, minute, hour = stringDelimit()
    # TODO: Change function based on mode
    addTime(second, minute, hour)

import tkinter as tk  # Basic TkInter
from tkinter import ttk  # Themed TkInter


def genWindow():
    digitColours = ['Black', 'Brown', 'Red', 'Orange', 'Yellow', 'Green',
                    'Blue', 'Violet', 'Grey', 'White']

    multiplyColours = ['Black', 'Brown', 'Red', 'Orange', 'Yellow', 'Green',
                       'Blue', 'Violet', 'Grey', 'White', 'Gold', 'Silver']

    toleranceColours = ['Brown', 'Red', 'Green',
                        'Blue', 'Violet', 'Grey', 'Gold', 'Silver']

    toleranceBand = {'Brown': '±1%', 'Red': '±2%', 'Green': '±0.5%',
                     'Blue': '±0.25%', 'Violet': '±0.1%', 'Grey': '±0.05%',
                     'Gold': '±5%', 'Silver': '±10%'}

    root = tk.Tk()
    root.title("Resistor Colour Code Calculator")
    root.resizable(False, False)

    digitStr0 = tk.StringVar(value="brown")
    digitStr1 = tk.StringVar(value="black")
    digitStr2 = tk.StringVar(value="")
    multStr = tk.StringVar(value="red")
    tolStr = tk.StringVar(value="gold")
    tempStr = tk.StringVar()
    resultStr = tk.StringVar(value="100")

    resistorFrame = ttk.LabelFrame(root, text="Resistor:")
    resistorFrame.pack(padx=20, pady=10, fill='x')

    resultFrame = ttk.LabelFrame(root, text="Result:")
    resultFrame.pack(padx=20, pady=10, fill='x')

    digitLabel0 = ttk.Label(
        resistorFrame, text="Digit 1").grid(row=0, column=0)
    digitLabel1 = ttk.Label(
        resistorFrame, text="Digit 2").grid(row=0, column=1)
    multiplyLabel = ttk.Label(
        resistorFrame, text="Multiply").grid(row=0, column=2)
    toleranceLabel = ttk.Label(
        resistorFrame, text="Tolerance").grid(row=0, column=3)

    digitBox0 = ttk.Combobox(resistorFrame, values=digitColours,
                             textvariable=digitStr0, width=7).grid(row=1, column=0, padx=5)
    digitBox1 = ttk.Combobox(resistorFrame, values=digitColours,
                             textvariable=digitStr1, width=7).grid(row=1, column=1, padx=5)
    multiplyBox = ttk.Combobox(resistorFrame, values=multiplyColours,
                               textvariable=multStr, width=7).grid(row=1, column=2, padx=5)
    toleranceBox = ttk.Combobox(resistorFrame, values=toleranceColours,
                                textvariable=tolStr, width=7).grid(row=1, column=3, padx=5)

    result = ttk.Label(resultFrame, text=resultStr.get())
    result.grid(row=0, column=2)

    goButton = ttk.Button(resultFrame, text="Calculate...",
                          command=lambda: [calculate(digitStr0.get(), digitStr1.get(), digitStr2.get(), multStr.get(), resultStr),
                                           result.config(text=resultStr.get() + 'Ω ' + toleranceBand.get(tolStr.get()))])
    goButton.grid(row=0, column=0)

    root.mainloop()


def calculate(digit0: str, digit1: str, digit2: str, mult: str, result):
    digitBand = {'Black': '0', 'Brown': '1', 'Red': '2', 'Orange': '3',
                 'Yellow': '4', 'Green': '5', 'Blue': '6', 'Violet': '7',
                 'Grey': '8', 'White': '9', 'Gold': '-1', 'Silver': '-1', '': ''}

    multiplyBand = {'Black': 1, 'Brown': 10, 'Red': 100, 'Orange': 1000,
                    'Yellow': 1e4, 'Green': 1e5, 'Blue': 1e6, 'Violet': 1e7,
                    'Grey': 1e8, 'White': 1e9, 'Gold': 0.1, 'Silver': 0.01}

    temperatureBand = {}

    result.set(str(int(digitBand.get(digit0) + digitBand.get(digit1) +
                       digitBand.get(digit2))*multiplyBand.get(mult)))


if __name__ == "__main__":

    genWindow()

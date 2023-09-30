import tkinter as tk  # Basic TkInter
from tkinter import ttk  # Themed TkInter


def genWindow(colours: str, digitBand: dict):
    root = tk.Tk()
    root.title("Resistor Colour Code Calculator")
    root.resizable(False, False)

    digitStr0 = tk.StringVar(value="brown")
    digitStr1 = tk.StringVar(value="black")
    multStr = tk.StringVar(value="red")
    tolStr = tk.StringVar(value="gold")
    tempStr = tk.StringVar()

    resistorFrame = ttk.LabelFrame(root, text="Resistor: ", )
    resistorFrame.pack(padx=20, pady=10, fill='x')

    digitLabel0 = ttk.Label(
        resistorFrame, text="Digit 1").grid(row=0, column=0)
    digitLabel1 = ttk.Label(
        resistorFrame, text="Digit 2").grid(row=0, column=1)
    multiplyLabel = ttk.Label(
        resistorFrame, text="Multiply").grid(row=0, column=2)
    toleranceLabel = ttk.Label(
        resistorFrame, text="Tolerance").grid(row=0, column=3)

    digitBox0 = ttk.Combobox(resistorFrame, values=colours,
                             textvariable=digitStr0, width=7).grid(row=1, column=0)
    digitBox1 = ttk.Combobox(resistorFrame, values=colours,
                             textvariable=digitStr1, width=7).grid(row=1, column=1)
    multiplyBox = ttk.Combobox(
        resistorFrame, values=colours, textvariable=multStr, width=7).grid(row=1, column=2)
    toleranceBox = ttk.Combobox(
        resistorFrame, values=colours, textvariable=tolStr, width=7).grid(row=1, column=3)

    root.mainloop()


if __name__ == "__main__":
    colours = ['black', 'brown', 'red', 'orange', 'yellow', 'green',
               'blue', 'violet', 'grey', 'white', 'gold', 'silver']

    digitBand = {'black': '0', 'brown': '1', 'red': '2', 'orange': '3',
                 'yellow': '4', 'green': '5', 'blue': '6', 'violet': '7',
                 'grey': '8', 'white': '9', 'gold': '-1', 'silver': '-1'}

    multiplyBand = {'black': 1, 'brown': 10, 'red': 100, 'orange': 1000,
                    'yellow': 1e4, 'green': 1e5, 'blue': 1e6, 'violet': 1e7,
                    'grey': 1e8, 'white': 1e9, 'gold': 0.1, 'silver': 0.01}

    toleranceBand = {'black': -1, 'brown': 1, 'red': 2, 'orange': -1,
                     'yellow': -1, 'green': 0.5, 'blue': 0.25, 'violet': 0.1,
                     'grey': 0.05, 'white': -1, 'gold': 5, 'silver': 10}

    temperatureBand = {}

    genWindow(colours, digitBand)

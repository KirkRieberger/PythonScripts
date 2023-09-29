import tkinter as tk  # Basic TkInter
from tkinter import ttk  # Themed TkInter


def genWindow(colours: str, digitBand: dict):
    digitStr = tk.StringVar

    root = tk.Tk()
    root.title("Resistor Colour Code Calculator")
    root.resizable(False, False)

    resistorFrame = ttk.LabelFrame(root, text="Resistor: ")
    resistorFrame.pack(padx=20, pady=10, fill='x')

    digitBox = ttk.Combobox(
        resistorFrame, values=colours, textvariable=digitStr, width=6)
    digitBox.pack(padx=5, pady=5)

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

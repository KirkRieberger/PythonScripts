import tkinter as tk
from tkinter import ttk


def genWindow():
    root = tk.Tk()
    root.title("Resistor Colour Code Calculator")
    root.resizable(False, False)

    root.mainloop()


if __name__ == "__main__":
    genWindow()

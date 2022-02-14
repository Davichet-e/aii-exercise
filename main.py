import tkinter as tk
from aii.data_access.db import DBHandler

from aii.presenter.desktop_presenter import App


WINDOW = tk.Tk()

APP = App(WINDOW)


def on_closing():
    WINDOW.destroy()
    DBHandler.destroy()


WINDOW.protocol("WM_DELETE_WINDOW", on_closing)

WINDOW.mainloop()

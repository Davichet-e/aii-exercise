import tkinter as tk
from aii.data_access.db import DBHandler

from aii.presenter.desktop_presenter import App


WINDOW = tk.Tk()

APP = App(WINDOW)

WINDOW.mainloop()

DBHandler.destroy()

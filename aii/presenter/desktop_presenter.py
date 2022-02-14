import tkinter as tk
from tkinter import messagebox
from typing import Callable

from aii.services.exceptions import (
    InternalErrorException,
    NewsNotStoredException,
    RetrieveNewsException,
)
from aii.services import news_service
from aii.entities.news import News
from aii.repositories.sqlite_repository import SQLiteRepository


class App:
    URL = "https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml"

    def __init__(self, master: tk.Tk) -> None:
        self._frame = tk.Frame(master=master)
        self._frame.grid()

        self._db_handler = SQLiteRepository()

        self._retrieve_button = tk.Button(
            self._frame, text="Almacenar", command=lambda: self.retrieve_news()
        )
        self._retrieve_button.grid(row=0, column=0)

        self._show_news_button = tk.Button(
            self._frame, text="Listar", command=lambda: self.show_news()
        )
        self._show_news_button.grid(row=0, column=1)

        self._filter_by_month_button = tk.Button(
            self._frame, text="Busca Mes", command=lambda: self.filter_by_month()
        )
        self._filter_by_month_button.grid(row=0, column=2)

        self._filter_by_day_button = tk.Button(
            self._frame, text="Busca Día", command=lambda: self.filter_by_day()
        )
        self._filter_by_day_button.grid(row=0, column=3)

        self.news: list[News] = None

    def retrieve_news(self):
        """Retrieve the news and display a message."""
        try:
            news_service.store_news(self.URL)
        except RetrieveNewsException as exception:
            text = str(exception)
        else:
            text = "BD creada correctamente"

        messagebox.showinfo("Información", text)

    def show_news(self):
        try:
            self.news = news_service.retrieve_news_from_db()
        except NewsNotStoredException:
            text = "Obtén las noticias primero, pulsa en `Almacenar`"

        except InternalErrorException:
            text = (
                "Hubo un error interno obteniendo las noticias.\n"
                "Por favor, intentelo de nuevo en unos minutos."
            )

        else:
            text = "\n\n".join(list(map(str, self.news)))

        ShowTextWindow(self._frame, text).grid()

    def filter_by_month(self):
        month_var = tk.StringVar()
        ShowFilterByWindow(
            self._frame,
            month_var,
            text="Introduzca el mes (Xxx): ",
            callback=lambda: self.show_news_filtered_by_month(month_var.get()),
        ).grid()

    def show_news_filtered_by_month(self, month: str):
        try:
            self.news = news_service.filter_news_by_month(month)

        except NewsNotStoredException:
            text = "Obtén las noticias primero, pulsa en `Almacenar`"

        else:
            if len(self.news) == 0:
                text = "No existen noticias con esa fecha"
            else:
                text = "\n\n".join(list(map(str, self.news)))

        ShowTextWindow(self._frame, text).grid()

    def filter_by_day(self):
        day_var = tk.StringVar()
        ShowFilterByWindow(
            self._frame,
            day_var,
            text="Introduzca el día (dd/mm/aaaa)",
            callback=lambda: self.show_news_filtered_by_day(day_var.get()),
        ).grid()

    def show_news_filtered_by_day(self, day: str):
        try:
            self.news = news_service.filter_news_by_day(day)

        except NewsNotStoredException:
            text = "Obtén las noticias primero, pulsa en `Almacenar`"

        else:
            if len(self.news) == 0:
                text = "No existen noticias con esa fecha"
            else:
                text = "\n\n".join(list(map(str, self.news)))

        ShowTextWindow(self._frame, text).grid()


class ShowFilterByWindow(tk.Toplevel):
    def callback(self, callback):
        callback()
        self.destroy()

    def __init__(self, master, str_var: tk.StringVar, text: str, callback: Callable):
        super().__init__(master)

        tk.Label(self, text=text).grid()
        month_input = tk.Entry(self, textvariable=str_var)
        month_input.grid(column=2, row=0)

        month_input.bind("<Return>", lambda _event: self.callback(callback))


class ShowTextWindow(tk.Toplevel):  # Create a window
    def __init__(self, master, text: str):
        super().__init__(master)
        tk.Label(self, text=text, anchor="w", justify=tk.LEFT).pack(side=tk.LEFT)

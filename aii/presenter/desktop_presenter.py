import tkinter as tk

from aii.repositories.exceptions import DatabaseException

from aii.data_handler.exceptions import RetrieveNewsException
from aii.data_handler.news_handler import retrieve_news
from aii.entities.news import News
from aii.repositories.sqlite_repository import DBHandler


class App:
    URL = "https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml"

    def __init__(self, master: tk.Tk) -> None:
        self._frame = tk.Frame(master=master)
        self._frame.grid()

        self._db_handler = DBHandler()

        self._retrieve_button = tk.Button(
            self._frame, text="Almacenar", command=lambda: self.retrieve_news()
        )
        self._retrieve_button.grid(row=0, column=0)

        self._show_news_button = tk.Button(
            self._frame, text="Listar", command=lambda: self.show_news()
        )
        self._show_news_button.grid(row=0, column=1)

        # self._filter_by_month_button = tk.Button(
        #     self._frame, text="Busca Mes", command=self.filter_by_month
        # )
        # self._filter_by_month_button.grid(x=2, y=0)

        # self._filter_by_day_button = tk.Button(
        #     self._frame, text="Busca Día", command=self.filter_by_day
        # )

        self.news: list[News] = None

    def retrieve_news(self):
        """Retrieve the news and display a message."""
        try:
            self.news = retrieve_news(self.URL)
        except RetrieveNewsException as exception:
            text = str(exception)
        else:
            text = "BD creada correctamente"

        tk.Label(self._frame, text=text).grid(column=0, row=1)

    def show_news(self):
        # FIXME When already in database, should just retrive from there
        if self.news is None:
            text = "Obtén las noticias primero, pulsa en `Almacenar`"
        else:
            text = "\n\n".join(list(map(str, self.news)))
        ShowTextWindow(self._frame, text).grid()


class ShowTextWindow(tk.Toplevel):  # Create a window
    def __init__(self, master, text: str):
        super().__init__(master)
        tk.Label(self, text=text,).pack()

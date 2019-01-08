# main_gui.py python3
""" This module is design to run the GUI main application.
The GUI is written in tkinter library.
"""


import tkinter as tk
import tkinter.font as tkfont
from gui.wiki_window import WikiMain
from gui.game_window import GameMain
from gui.stat_window import StatMain


class Application(tk.Tk):
    """This class runs the GUI tkinter application."""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame(StartPage)

    def show_frame(self, cls):
        """Show a frame for the given page name"""
        frame = cls(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class StartPage(tk.Frame):
    """This is the menu page that redirects to thw following windows:
        1. Wiki - wiki window that allows you to search, view, delete and add new words from WikiMedia
        2. Start Game - open and initialize game
        3. Statistics - show the game statistics
        4. Quit - terminate the application
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_start = tk.Label(self, text="Welcome to WikiBase!", font=controller.title_font)
        label_start.pack(side='top', fill='x', padx=15, pady=10)

        helv36 = tkfont.Font(family='Helvetica', size=12, weight='bold')

        btn_wiki = tk.Button(self, text="Wiki", command=lambda: controller.show_frame(WikiPage))
        btn_wiki.configure(heigh=3, width=20, font=helv36)

        btn_game = tk.Button(self, text="Start Game", command=lambda: controller.show_frame(GamePage))
        btn_game.configure(heigh=3, width=20, font=helv36)

        btn_stat = tk.Button(self, text="Statistic", command=lambda: controller.show_frame(StatPage))
        btn_stat.configure(heigh=3, width=20, font=helv36)

        btn_quit = tk.Button(self, text="Exit", command=self.quit)
        btn_quit.configure(heigh=3, width=20, font=helv36)

        btn_wiki.pack(anchor=tk.CENTER, padx=10, pady=10)
        btn_game.pack(anchor=tk.CENTER, padx=10, pady=10)
        btn_stat.pack(anchor=tk.CENTER, padx=10, pady=10)
        btn_quit.pack(anchor=tk.CENTER, padx=10, pady=10)


class WikiPage(WikiMain):
    """Initialize and open Wiki window."""

    def __init__(self, parent, controller):
        WikiMain.__init__(self, parent)
        self.controller = controller
        self.btn_home['command'] = lambda: controller.show_frame(StartPage)


class GamePage(GameMain):
    """Initialize and open Game window."""

    def __init__(self, parent, controller):
        GameMain.__init__(self, parent)
        self.controller = controller
        self.btn_home['command'] = lambda: controller.show_frame(StartPage) if self.exit_game_window() is True else None


class StatPage(StatMain):
    """Initialize and open Statistics window."""

    def __init__(self, parent, controller):
        StatMain.__init__(self, parent)
        self.controller = controller
        self.btn_home['command'] = lambda: controller.show_frame(StartPage)


if __name__ == '__main__':
    app = Application()
    app.geometry('600x600')
    app.title('WikiBase')
    app.mainloop()


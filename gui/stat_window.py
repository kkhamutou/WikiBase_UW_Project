#!gui/stat_window.py python3
""""
This module is used to create Statistics Frame and to demonstrate all statistics collected from games.
"""

import tkinter as tk
import tkinter.messagebox as msg
from gui.widgets.multi_listbox import MultiColumnListBox
from constants import DB_PATH
from repository.db_setup import Repository


class StatMain(tk.Frame):
    """StatMain is a frame and """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        fm_top = tk.Frame(self)
        fm_top.pack(side=tk.TOP, fill=tk.X, pady=20, padx=5)

        self.btn_home = tk.Button(fm_top, text='Home')
        self.btn_home.pack(side=tk.LEFT)

        self.repo = Repository(DB_PATH)

        self.listbox = MultiColumnListBox(self, headers=['Stat', 'Value'])
        self.listbox.pack(fill=tk.X, expand=True, anchor=tk.N, padx=10, pady=10)

        self.btn_reset = tk.Button(self.listbox, text='Reset Stat', command=self.clean_stat)
        self.btn_reset.grid(pady=10)

        self._build_tree()

    def _build_tree(self):
        """Retrieve statistics from the database and insert it to listbox"""
        res = self.repo.get_stat()

        for attr in res._fields:
            self.listbox.tree.insert('', tk.END, values=[f'{attr}'.replace('_', ' '), getattr(res, attr)])

    def clean_stat(self):
        """Clear listbox and statistics table in the database"""
        exit_msg = msg.askquestion('Warning',
                                   'Are you sure you want to reset your statistics?\nYou data will be lost.')

        if exit_msg == 'yes':
            self.listbox.tree.delete(*self.listbox.tree.get_children())
            self.repo.del_stat()
            self._build_tree()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x600')
    x = StatMain(root)
    x.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
    x.mainloop()

import tkinter as tk
import tkinter.ttk as ttk
from functools import reduce
from repository.db_setup import Repository


_FILTER_NAMES = ['title', 'search_word', 'added_date']
_FILTER_CRITERIA_DATE = ['Between', 'Is equal to', 'Is not equal to', 'Greater', 'Greater or equal to',
                         'Less', 'Less or equal to']
_FILTER_CRITERIA_STRING = ['Is equal to', 'Is not equal to', 'Starts with', 'Ends with',
                           'Does not contain', 'Contains']



def apply_filter(parent):
    x = map(lambda z: z.set(''), (filter(lambda y: type(y) in (ttk.Entry, ttk.Combobox), parent.children.values())))
    print(x)


def f(parent):
    """Create label, combobox and entry widgets on a sub_frame of ToggledFrame
    and assign Repository.filter_by method to a button <Apply>"""

    for index, text in enumerate(_FILTER_NAMES):
        tk.Label(parent, text=text.replace('_', ' ').capitalize()).grid(row=index, column=0, pady=5, sticky=tk.W)
        ttk.Combobox(parent, values=_FILTER_CRITERIA_STRING if text != 'created_date' else
                     _FILTER_CRITERIA_DATE, state='readonly').grid(row=index, column=1, padx=7, pady=2)
        entry = ttk.Entry(parent)
        entry.grid(row=index, column=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=7, pady=2)
        tk.Grid.columnconfigure(parent, entry, weight=1)

    sub_frame = tk.Frame(parent)
    sub_frame.grid(row=4, column=2, sticky=tk.E, padx=3)

    tk.Button(sub_frame, text='Apply', command=lambda: apply_filter(parent)).grid(row=1, column=1, sticky=tk.E, padx=5)
    tk.Button(sub_frame, text='Reset').grid(row=1, column=2, sticky=tk.E, padx=5)


if __name__ == '__main__':

    root = tk.Tk()
    f(root)
    root.mainloop()
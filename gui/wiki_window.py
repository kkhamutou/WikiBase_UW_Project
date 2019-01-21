import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from api.wiki_service import WikiHttp, WikiService, Repository
from os import name as os_name
from gui.widgets.toggled_frame import ToggledFrame
from gui.widgets.multi_listbox import MultiColumnListBox, RightClick
from constants import DB_PATH


class ListboxRightClick(RightClick):

    def __init__(self, parent: ttk.Treeview, repo: Repository):
        RightClick.__init__(self, parent)
        self.aMenu.delete('Edit')
        self.repo = repo

    def view(self):
        word, meaning = self.tree.item(self.iid)['values'][2:5:2]
        msg.showinfo(word, meaning)

    def delete(self):
        self.repo.delete((self.tree.item(self.iid)['values'][0], ))
        self.tree.delete(self.iid)

    def edit(self):
        pass


class WikiMain(tk.Frame):

    _FILTER_NAMES = ['title', 'search_word', 'created_date']
    _FILTER_CRITERIA_DATE = ['Is equal to', 'Is not equal to', 'Greater', 'Greater or equal to',
                             'Less', 'Less or equal to']
    _FILTER_CRITERIA_STRING = ['Is equal to', 'Is not equal to', 'Starts with', 'Ends with',
                               'Does not contain', 'Contains']
    _COLUMN_DISPLAY = [0, 2, 3, 5]
    _COLUMN_NAMES = ['Id', 'Wiki Id', 'Title', 'Search word', 'Meaning', 'Created date']

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.window_add = None
        self.frame_add = None
        print(DB_PATH)
        self.repo = Repository(DB_PATH)

        frame_top = tk.Frame(self)
        frame_top.pack(side=tk.TOP, fill=tk.X, pady=20, padx=5)

        self.btn_home = tk.Button(frame_top, text='Home')
        self.btn_home.pack(side=tk.LEFT)

        self.btn_add = tk.Button(frame_top, text='Add', command=self.open_top_window)
        self.btn_add.pack(side=tk.RIGHT)

        self.tf = ToggledFrame(self, text='Filter', relief='raised', borderwidth=1)
        self._filter_entry()
        self.tf.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)

        self.listbox = MultiColumnListBox(self, headers=WikiMain._COLUMN_NAMES,
                                          displaycolumns=WikiMain._COLUMN_DISPLAY)
        self.listbox.pack(fill=tk.X, pady=15, padx=5)

        self.listbox.tree.bind('<Button-{}>'.format(3 if os_name == 'nt' else 2),
                               ListboxRightClick(self.listbox.tree, self.repo).popup)

        self.update_listbox()

    def _filter_entry(self):
        """Create label, combobox and entry widgets on a sub_frame of ToggledFrame
        and assign Repository.filter_by method to a button <Apply>"""

        for index, text in enumerate(WikiMain._FILTER_NAMES):
            tk.Label(self.tf.sub_frame,
                     text=text.replace('_', ' ').capitalize()).grid(row=index, column=0, pady=5, sticky=tk.W)

            # If label name == created_date, than the combobox values == _FILTER_CRITERIA_DATE
            ttk.Combobox(self.tf.sub_frame, values=WikiMain._FILTER_CRITERIA_STRING if text != 'created_date' else
                         WikiMain._FILTER_CRITERIA_DATE, state='readonly').grid(row=index, column=1, padx=7, pady=2)

            entry = ttk.Entry(self.tf.sub_frame)
            entry.grid(row=index, column=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=7, pady=2)
            tk.Grid.columnconfigure(self.tf.sub_frame, entry, weight=1)

        sub_frame = tk.Frame(self.tf.sub_frame)
        sub_frame.grid(row=4, column=2, sticky=tk.E, padx=3)

        tk.Button(sub_frame, text='Apply', command=self._apply_filter).grid(row=1, column=1, sticky=tk.E, padx=5)
        tk.Button(sub_frame, text='Reset', command=self._clean_filter).grid(row=1, column=2, sticky=tk.E, padx=5)

    def _apply_filter(self):
        """Check values of all filter widgets (expect <Apply> and <Reset> buttons).
        If these values satisfied two criteria (combobox != NULL and Entry != Null),
        the listbox is filtered."""

        widget_values = [[None] * 3 for _ in range(len(WikiMain._FILTER_NAMES))]

        for w in self.tf.sub_frame.children.values():
            row, column = int(w.grid_info()['row']), int(w.grid_info()['column'])

            if row <= len(WikiMain._FILTER_NAMES):
                widget_values[row][column] = WikiMain._FILTER_NAMES[row] if column == 0 else w.get().strip()

        r = [row for row in widget_values if all(row)]
        if not len(r):
            msg.showwarning('Warning', 'Please, select criteria and enter a value.')
        else:
            res = list(map(tuple, zip(*r)))
            self.listbox.tree.delete(*self.listbox.tree.get_children())
            self.listbox.build_tree(self.repo.filter_by(res[0], res[1], res[2]))

    def _clean_filter(self):
        """Clean all filtering criteria in widgets and reset listbox to 'find_all' state."""

        for widget in self.tf.sub_frame.children.values():
            if type(widget) == ttk.Combobox:
                widget.set('')
            elif type(widget) == ttk.Entry:
                widget.delete(0, 'end')

        self.update_listbox()

    def update_listbox(self):
        self.listbox.tree.delete(*self.listbox.tree.get_children())
        self.listbox.build_tree(self.repo.find_all())

    def open_top_window(self):

        if (self.window_add is not None) and self.window_add.winfo_exists():
            self.window_add.destroy()

        self.window_add = tk.Toplevel()

        self.window_add.geometry('600x300')
        self.window_add.title('Add new word')

        self.frame_add = AddWindow(self.window_add)
        self.frame_add.pack(fill=tk.BOTH, expand=True)
        self.window_add.bind("<Destroy>", lambda _: self.update_listbox() if self.frame_add.isAdded is True else None)


class AddWindow(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        frame_top = tk.Frame(self)
        frame_top.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)

        frame_bottom = tk.Frame(self)
        frame_bottom.pack(side=tk.TOP, expand=True, fill=tk.X, padx=10)

        self.isAdded = False

        self.notepad = tk.Text(frame_top, height=14, width=40, relief=tk.SUNKEN, borderwidth=1)
        self.notepad.pack(side=tk.LEFT, fill=tk.X, padx=4, pady=5)

        self.listbox = MultiColumnListBox(frame_top, show='tree')
        self.listbox.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=1, pady=5)

        self.button_reset = tk.Button(frame_bottom, text='Clear',
                                      command=lambda: [self.listbox.clear(), self.notepad.delete('1.0', tk.END)])
        self.button_reset.grid(row=0, column=1)

        self.button_add = tk.Button(frame_bottom, text='Add', command=self.read_notepad)
        self.button_add.grid(row=0, column=2, sticky=tk.W)

        self.button_close = tk.Button(frame_bottom, text='Close', command=parent.destroy)
        self.button_close.grid(row=0, column=3, sticky='ne')

    def read_notepad(self):

        self.listbox.clear()

        if not len(self.notepad.get('1.0', 'end-1c').strip()):
            msg.showwarning("Error", "Please, enter a value!")
        else:
            wiki_service = WikiService(wiki_http=WikiHttp(),
                                       repo=Repository(DB_PATH))
            words = [word for word in self.notepad.get('1.0', 'end-1c').split('\n') if len(word) > 0]
            suc, failed = wiki_service.get_meanings_from_wiki(wiki_service.check_database(words))

            if len(suc) > 0:
                self.isAdded = True

            d = dict()
            for cls in failed+suc:
                d.setdefault(cls.__class__.__name__, []).append(getattr(cls, 'title'))

            self.listbox.build_tree_from_dict(d)


if __name__ == '__main__':

    root = tk.Tk()
    root.geometry('600x600')
    x = WikiMain(root)
    x.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
    root.mainloop()


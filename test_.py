import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from api.wiki_service import WikiService, WikiHttp, Repository


class Notepad(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.notepad = tk.Text(self)
        self.notepad.pack(fill=tk.BOTH, expand=True)

    def retrieve_input(self):
        print(self.notepad.get('1.0', 'end-1c'))


class Tree(tk.Frame):

    def __init__(self, parent, headers=None,  displaycolumns=None):
        super().__init__(parent)

        self.tree = ttk.Treeview(parent, show='headings')

        if headers is not None:
            self.tree['column'] = headers

        if displaycolumns is not None:
            self.tree['displaycolumns'] = displaycolumns

        for header in self.tree['column']:
            self.tree.heading(header, text=header.title())
            self.tree.column(header, width=tkFont.Font().measure(header.title()), anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def build_tree(self, items):

        for key, item in items.items():

            row_id = self.tree.insert('', tk.END, text=key)

            for value in item:
                self.tree.insert(row_id, tk.END, text=value)
                col_width = tkFont.Font().measure(value)

                if self.tree.column('#0', width=None) < col_width:
                    self.tree.column('#0', width=col_width)


def add_words(notepad: tk.Text, tree: Tree):

    if len(notepad.get('1.0', 'end-1c').strip()) == 0:
        raise ValueError

    tree.tree.delete(*tree.tree.get_children())

    words = notepad.get('1.0', 'end-1c').split('\n')
    service = WikiService(wiki_http=WikiHttp(), repo=Repository())
    suc, failed = service.get_meanings_from_wiki(words)

    d = dict()
    for klass in failed:
        d.setdefault(klass.__class__.__name__, []).append(getattr(klass, 'title'))

    tree.build_tree(d)



if __name__ == '__main__':
    root = tk.Tk()


    #image = tk.Image(file='/Users/kirylkhamutou/IdeaProjects/WikiBase_UW_Project/gui/images/wiki_logo.png')
    #fm = tk.Frame(root, image=image)
    #fm.pack()
    btn_add = tk.Button(root, text='i')
    btn_add.pack(side=tk.TOP, expand=True, )

    notepad = Notepad(root)
    notepad.pack(side=tk.LEFT, expand=True)

    tree = Tree(root)
    tree.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

    btn_add = tk.Button(root, text='Add',
                        command=lambda: add_words(notepad.notepad, tree))
    btn_add.pack()

    root.mainloop()

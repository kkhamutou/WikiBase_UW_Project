#!/multi_listbox.py Python3
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.messagebox as msg
from os import name as os_name


class MultiColumnListBox(tk.Frame):

    def __init__(self, parent, headers=None, displaycolumns=None):

        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 15))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tree = ttk.Treeview(self, show='headings', style="mystyle.Treeview")

        if headers is not None:
            self.tree['column'] = headers

        if displaycolumns is not None:
            self.tree['displaycolumns'] = displaycolumns

        vsb = tk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        hsb = tk.Scrollbar(self, orient='horizontal', command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=1, sticky='nsew')

        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        for header in self.tree['column']:
            self.tree.heading(header, text=header.title(),
                              command=lambda c=header: sortby(self.tree, c, False))
            self.tree.column(header, width=tkFont.Font().measure(header.title()), anchor=tk.CENTER)

    def build_tree(self, items):

        for item in items:
            self.tree.insert('', tk.END, values=item)   # tags=('odd' if row % 2 == 0 else 'even', )

            for index, value in enumerate(item):
                col_width = tkFont.Font().measure(value)
                if self.tree.column(self.tree['column'][index], width=None) < col_width:
                    self.tree.column(self.tree['column'][index], width=col_width)

        # self.tree.tag_configure('odd', background='#E8E8E8', font=("Verdana", 8))
        # self.tree.tag_configure('even', background='#DFDFDF', font=("Verdana", 8))


class RightClick:
    def __init__(self, parent):

        self.tree = parent
        self.iid = None
        self.aMenu = tk.Menu(parent, tearoff=0)

        self.aMenu.add_command(label='View', command=self.view)
        self.aMenu.add_command(label='Edit', command=self.edit)
        self.aMenu.add_command(label='Delete', command=self.delete)

    def view(self):
        raise NotImplementedError

    def edit(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def popup(self, event):
        self.iid = self.tree.identify_row(event.y)
        if self.iid:
            self.tree.selection_set(self.iid)
            self.aMenu.post(event.x_root, event.y_root)


# Better to leave it as it is or do it in database!?
def sortby(tree, col, reverse: bool):
    """Sort tree contents when a column header is clicked on"""

    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    data.sort(reverse=reverse)

    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)

    tree.heading(col, command=lambda col=col: sortby(tree, col, not reverse))


if __name__ == '__main__':

    from test_cases.case_listbox import CaseListbox

    test_case = CaseListbox().case_data(4)
    col_headers = ['Id', 'Wiki Id', 'Title', 'Search word', 'Added date']

    root = tk.Tk()
    root.geometry('600x400')
    listbox = MultiColumnListBox(root, col_headers, [0, 2, 3, 4])
    listbox.build_tree(test_case)
    listbox.tree.bind('<Button-{}>'.format(3 if os_name == 'nt' else 2), RightClick(listbox.tree).popup)
    listbox.pack()
    root.mainloop()

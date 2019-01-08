#!gui/widgets/multi_listbox.py Python3
"""
This module stores MultiColumnListBox widget (customized version of ttk.Treeview) and
RightClick abstract class designed for the right click mouse event.
MultiColumnListBox inherits from tk.Frame, which in fact makes this class a frame object. In order ot get access to
Tree, you need to call MultiColumnListBox.tree
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont


class MultiColumnListBox(tk.Frame):
    """Custom version of ttk.Treeview widget based on tk.Frame
    Args:
        parent: tk.Frame, tk.TopWindow, the parent object that host the tk.Frame
            (could be another frame, top-level window, mainWindow and etc.)
        headers: list, Header of your listbox, default=None (e.g. ['Column1', 'Column2', 'Column3'].
        displaycolumns: list, columns to be displayed from headers
            (e.g. [0, 2] will display only ['Column1', 'Column3'], but the access to 'Column2' is still possible.
        show: str, type of representation of your columns, default='headings' (see ttk.TreeView show documentation).
        """

    def __init__(self, parent, headers=None, displaycolumns=None, show='headings'):

        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 10))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 11))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tree = ttk.Treeview(self, show=show, style="mystyle.Treeview")

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

    def build_tree(self, items: list):
        """Build treeview from nested lists
        Args:
            items: list, items to be inserted into treeview
        """
        for item in items:
            self.tree.insert('', tk.END, values=item)

            for index, value in enumerate(item):
                col_width = tkFont.Font().measure(value)
                if self.tree.column(self.tree['column'][index], width=None) < col_width:
                    self.tree.column(self.tree['column'][index], width=col_width)

    def build_tree_from_dict(self, items: dict):
        """build treeview for dict
        Args:
            items: dict, items to be inserted into treeview
        """
        for key, item in items.items():

            row_id = self.tree.insert('', tk.END, text=key)

            for value in item:
                self.tree.insert(row_id, tk.END, text=value)
                col_width = tkFont.Font().measure(value)

                if self.tree.column('#0', width=None) < col_width:
                    self.tree.column('#0', width=col_width)

    def clear(self):
        """release treeview (delete all items)"""
        self.tree.delete(*self.tree.get_children())


class RightClick:
    """Abstract class for Right click even for treeview. Provides menu with 3 options: View, Edit and Delete."""
    def __init__(self, parent):

        self.tree = parent
        self.iid = None
        self.aMenu = tk.Menu(parent, tearoff=0)

        self.aMenu.add_command(label='View', command=self.view)
        self.aMenu.add_command(label='Edit', command=self.edit)
        self.aMenu.add_command(label='Delete', command=self.delete)

    def view(self):
        """View method. To be implemented."""
        raise NotImplementedError

    def edit(self):
        """Edit method. To be implemented."""
        raise NotImplementedError

    def delete(self):
        """delete method. To be implemented."""
        raise NotImplementedError

    def popup(self, event):
        """Show option after a right click on treeview"""
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
    listbox = MultiColumnListBox(root, show='tree')
    d = {'MissingResponse': ['Jack', 'Crack'],
         'InvaludResponse': ['Pythoningf', 'sadas', '[][][][']}

    listbox.build_tree_from_dict(d)
    listbox.pack()
    root.mainloop()

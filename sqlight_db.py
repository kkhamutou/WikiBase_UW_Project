import tkinter as tk
import tkinter.scrolledtext as ScrolledText
import tkinter.ttk as ttk


class Notepad(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.text_area = ScrolledText.ScrolledText(self, width=40)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    # root = tk.Tk()
    # root.geometry('600x600')
    # f1 = tk.Frame(root)
    # f2 = tk.Frame(root)
    #
    # f2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # # f1.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
    # # tree = ttk.Treeview(f1)
    # # tree.pack(fill=tk.BOTH, expand=True)
    # Notepad(f2).pack()
    #
    # root.mainloop()


    win = tk.Tk()

    win.configure(background="#808000")

    frame1 = tk.Frame(win,width=80, height=80,bg = '#ffffff',
                      borderwidth=1, relief="sunken")
    scrollbar = tk.Scrollbar(frame1)
    editArea = tk.Text(frame1, width=20, height=40, wrap="word",
                       yscrollcommand=scrollbar.set,
                       borderwidth=0, highlightthickness=0)
    scrollbar.config(command=editArea.yview)
    scrollbar.pack(side="right", fill="y")
    editArea.pack(side="left", fill="both", expand=True)
    frame1.place(x=10,y=30)

    win.mainloop()
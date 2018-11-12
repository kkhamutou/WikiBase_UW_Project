import tkinter as tk
import tkinter.font as tkfont


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        btn_return = tk.Button(self, text="Return to the start page",
                               command=lambda: controller.show_frame("StartPage"))
        btn_return.pack(side=tk.BOTTOM)


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = dict()
        for F in (StartPage, WikiPage, GamePage, OptionPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label_start = tk.Label(self, text="Welcome to WikiBase!", font=controller.title_font)
        label_start.pack(side='top', fill='x', padx='10')

        btn_wiki = tk.Button(self, text="Wiki", command=lambda: controller.show_frame("WikiPage"))
        btn_game = tk.Button(self, text="Game", command=lambda: controller.show_frame("GamePage"))
        btn_option = tk.Button(self, text="Option", command=lambda: controller.show_frame("OptionPage"))
        btn_quit = tk.Button(self, text="Exit", command=self.quit)

        btn_wiki.pack()
        btn_game.pack()
        btn_option.pack()
        btn_quit.pack()


class WikiPage(MainPage):

    def __init__(self, parent, controller):
        MainPage.__init__(self, parent, controller)
        label_start = tk.Label(self, text="Wiki Page!", font=controller.title_font)
        label_start.pack(side='top', fill='x', padx='10', pady='30')

        frame_listbox = tk.Frame(self)
        frame_listbox.pack()

        scrollbar = tk.Scrollbar(frame_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame_listbox, width=50, height=10)
        listbox.pack()

        for i in range(100):
            listbox.insert(tk.END, i)

        # attach listbox to scrollbar
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)


class GamePage(MainPage):

    def __init__(self, parent, controller):
        MainPage.__init__(self, parent, controller)
        label_start = tk.Label(self, text="Game Page!", font=controller.title_font)
        label_start.pack(side='top', fill='x', padx='10')


class OptionPage(MainPage):

    def __init__(self, parent, controller):
        MainPage.__init__(self, parent, controller)
        label_start = tk.Label(self, text="Option Page!", font=controller.title_font)
        label_start.pack(side='top', fill='x', padx='10')


class TreeView(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(master=master)




if __name__ == '__main__':
    app = Application()
    app.geometry('600x600')
    app.mainloop()


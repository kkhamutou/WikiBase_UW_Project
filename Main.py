from gui.main_gui import Application
import tkinter.messagebox as msg
from __setup__ import demo_setup


def _install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


if __name__ == '__main__':

    _install_and_import("requests")
    app = Application()
    app.geometry('800x600')
    app.title('WikiBase')

    demo = msg.askquestion("Test case", "Would you like to use Demo?\nIt's highly recommended.\nUse only once!")
    if demo == 'yes':
        demo_setup()

    app.mainloop()

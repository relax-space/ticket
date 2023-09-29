from tkinter import Label, Tk,Menu

def init_view():
    global root
    root = Tk()
    menubar = Menu(root)
    activer = Menu(menubar,tearoff=0)
    menubar.add_cascade(label='文件',menu=activer)
    activer.add_command()
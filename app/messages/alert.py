import tkinter.messagebox as msgbox


def show_error(message, title="Error"):
    msgbox.showerror(title, message)


def show_warning(message, title="Warning"):
    msgbox.showwarning(title, message)


def show_info(message, title="Info"):
    msgbox.showinfo(title, message)

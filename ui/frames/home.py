from tkinter import *

from ui.dialogs.research import ResearchDialog

def nothing():
    print("TO DO")

class HomeFrame(Frame):    

    def __init__(self, parent, controller, additional_args):
        Frame.__init__(self, parent)
        self.controller = controller

        self.menubar = Menu(parent)

        menu1 = Menu(self.menubar, tearoff=0)
        menu1.add_command(label="Ajouter", command=lambda: controller.show_dialog(ResearchDialog))
        menu1.add_command(label="Editer", command=nothing)
        menu1.add_command(label="Supprimer", command=nothing)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=controller.destroy)
        self.menubar.add_cascade(label="Livres", menu=menu1)

        menu2 = Menu(self.menubar, tearoff=0)
        menu2.add_command(label="Gérer", command=nothing)
        self.menubar.add_cascade(label="Tags", menu=menu2)

        menu3 = Menu(self.menubar, tearoff=0)
        menu3.add_command(label="Par tags", command=nothing)
        menu3.add_command(label="Par auteurs", command=nothing)
        menu3.add_separator()
        menu3.add_command(label="Supprimer filtres", command=nothing)
        self.menubar.add_cascade(label="Filtrer", menu=menu3)
        
        label = Label(self, text="This is the home page", font=controller.title_font)
        label.pack(side=TOP, fill=X, pady=10)
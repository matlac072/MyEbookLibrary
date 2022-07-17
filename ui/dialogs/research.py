from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showinfo

from ui.frames.results import ResultsFrame

class ResearchDialog():

    def __init__(self, controller):
        self.controller = controller

        top = self.top = Toplevel(controller, width=250, height=250)
        top.title("Chercher un livre")

        main_label = Label(top, text="Chercher un livre", font=Font(family="Helvetica", size=18, weight="bold"))
        main_label.pack(side=TOP, pady=10)

        labeled_frame = LabelFrame(top, text="Options", padx=10, pady=10)

        search_options = self.search_options = StringVar()
        radio1 = Radiobutton(labeled_frame, text="Par titre", variable=search_options, value='title')
        radio2 = Radiobutton(labeled_frame, text="Par auteur", variable=search_options, value='author')
        radio3 = Radiobutton(labeled_frame, text="Par mots-clés", variable=search_options, value='keywords')
        search_options.set('title')
        radio1.pack(anchor=W)
        radio2.pack(anchor=W)
        radio3.pack(anchor=W)
        labeled_frame.pack(fill=X, padx=30)
        
        entrybox = self.entrybox = Entry(top, width=30)
        entrybox.pack(fill=X, padx=30, pady=10)
        entrybox.focus()

        submit_button = self.submit_button = Button(top, text="Rechercher", command=self.send)
        submit_button.pack()

        top.bind("<Return>", self.send)

        self.center_dialog()

    def center_dialog(self):
        screen_width = self.controller.winfo_screenwidth()
        screen_height = self.controller.winfo_screenheight()
        x = screen_width / 2 - self.top.winfo_reqwidth() / 2
        y = screen_height / 2 - self.top.winfo_reqheight() / 2
        self.top.geometry('%dx%d+%d+%d' % (self.top.winfo_reqwidth(), self.top.winfo_reqheight(), x, y))

    def send(self, event=None):
        if event != None:
            self.submit_button.configure(relief=SUNKEN)
            self.submit_button.update()

        self.search_entry = self.entrybox.get()

        if not self.search_entry.strip() == "":
            self.chosen_search_option = self.search_options.get()

            if self.chosen_search_option == 'keywords':
                results = self.search_results = self.controller.api_client.search_from_keywords(self.search_entry)
            elif self.chosen_search_option == 'title':
                results = self.search_results = self.controller.api_client.search_from_title(self.search_entry)
            elif self.chosen_search_option == 'author':
                results = self.search_results = self.controller.api_client.search_from_author(self.search_entry)
            else:
                print("Something bad happened !")
                self.top.destroy()
                self.controller.destroy()
            
            self.controller.show_frame(ResultsFrame, [results])
            self.top.destroy()

        else:
            showinfo("Erreur", "Ce champ ne peut pas être vide !")
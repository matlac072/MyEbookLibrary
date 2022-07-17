from tkinter import *
import math

from ui.frames.home import HomeFrame
from utils.cover_download import get_cover_from_url
from config import MAX_RESULTS_DISPLAYED

class ResultsFrame(Frame):

    def __init__(self, parent, controller, additionnal_args):
        Frame.__init__(self, parent)
        self.controller = controller

        self.menubar = Menu(parent)

        menu1 = Menu(self.menubar, tearoff=0)
        menu1.add_command(label="Retour à la librairie", command=lambda: controller.show_frame(HomeFrame))
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=controller.destroy)
        self.menubar.add_cascade(label="Annuler", menu=menu1)

        self.results = additionnal_args[0]
        self.covers = []

        scrollbar = Scrollbar(parent, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y, expand=0)

        canvas = self.canvas = Canvas(parent, bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
        canvas.pack(fill=BOTH, expand=TRUE)
        scrollbar.configure(command=canvas.yview)
        
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        
        scrollable_frame = self.scrollable_frame = Frame(canvas)
        canvas.create_window((0,0), 
            window=scrollable_frame, 
            anchor=NW, 
            width=controller.winfo_screenwidth()
        )

        self.page_index = 0
        self.pages_count = max(0, math.ceil(len(self.results) / MAX_RESULTS_DISPLAYED) - 1)
        self.display_results()

        scrollable_frame.bind("<Configure>", self.onCanvasConfigure)
        scrollable_frame.bind("<Enter>", self._bound_to_mousewheel)
        scrollable_frame.bind("<Leave>", self._unbound_to_mousewheel)

    def onCanvasConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def display_results(self):

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        results_frame = Frame(self.scrollable_frame)
        results_frame.pack(side=TOP, fill=X)

        buttons_frame = Frame(self.scrollable_frame)
        buttons_frame.pack(side=BOTTOM)

        row = 1
        column = 1
        for book in self.results[self.page_index:min(self.page_index + MAX_RESULTS_DISPLAYED, len(self.results))]:
            book_cover = get_cover_from_url(book.cover_url)
            book_frame = Frame(results_frame)
            book_frame.grid(row=row, column=column)

            label = Label(book_frame, image=book_cover)
            label.image = book_cover
            label.pack(padx=10, pady=10)
            self.covers.append(label)

            column += 1
            if column > 4:
                row += 1
                column = 1

        previous_page_button = Button(buttons_frame, text="Page précédente", command=self.goto_previous_page)
        next_page_button = Button(buttons_frame, text="Page suivante", command=self.goto_next_page)

        state = DISABLED if self.page_index == 0 else NORMAL
        previous_page_button.configure(state=state)

        state = DISABLED if self.page_index == self.pages_count else NORMAL
        next_page_button.configure(state=state)

        previous_page_button.grid(row=1, column=0, padx=5)
        next_page_button.grid(row=1, column=1, padx=5)

    def goto_previous_page(self):
        self.page_index -= 1
        self.display_results()
        self.scrollable_frame.update()
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    def goto_next_page(self):
        self.page_index += 1
        self.display_results()
        self.scrollable_frame.update()
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

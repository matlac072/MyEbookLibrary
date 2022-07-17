from tkinter import *
from tkinter import font as tkfont

from config import WIN_WIDTH, WIN_HEIGHT

from ui.frames.home import HomeFrame

class App(Tk):

    def __init__(self, db, api_client):
        Tk.__init__(self)

        self.db = db
        self.api_client = api_client

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("My Ebook Library")

        self.center_window()
        self.state('zoomed')

        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self._frame = None
        self.show_frame(HomeFrame)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width / 2 - WIN_WIDTH / 2
        y = screen_height / 2 - WIN_HEIGHT / 2
        self.geometry('%dx%d+%d+%d' % (WIN_WIDTH, WIN_HEIGHT, x, y))

    def show_frame(self, frame_class, additional_args=[]):
        new_frame = frame_class(self.container, self, additional_args)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        self.configure(menu=self._frame.menubar)

    def show_dialog(self, dialog_class):
        dialog = dialog_class(self)
        self.wait_window(dialog.top)
        
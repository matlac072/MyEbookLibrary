from ui.app import App    
from data.handler import DatabaseHandler
from data.openlibrary import OpenLibraryAPIClient

if __name__=="__main__":
    db = DatabaseHandler()
    api_client = OpenLibraryAPIClient()

    app = App(db, api_client)
    app.mainloop()
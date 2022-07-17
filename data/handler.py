import json
import os

from pydantic import BaseModel
from typing import List, Optional

from config import LIBRARY_DATABASE

class BookEntry(BaseModel):
    olid: str
    title: str
    author: List[str] = []
    number_of_pages: Optional[int]
    publish_year: Optional[int]
    cover_url: str
    cover_cache_path: Optional[str]

class Books(BaseModel):
    books: List[BookEntry] = []

class DatabaseHandler():
    
    def __init__(self):
        # If DB does not exist we create it
        if not os.path.isfile(LIBRARY_DATABASE):
            with open(LIBRARY_DATABASE, "w") as f:
                json.dump(Books().dict(), f)


import requests
import json
import traceback

from config import REQUESTS_TIMEOUT
from data.handler import BookEntry

def add_query_items(url, query_items):
    for item in query_items.keys():
        url = url + "?" + item + "=" + query_items[item].replace(" ","+")
    return url

class OpenLibraryAPIClient():

    def __init__(self):
        self.base_url = "http://openlibrary.org/"
        self.search_url = self.base_url + "search.json"
        self.book_url = self.base_url + "api/books.json"

    def get_books_info(self, data):
        books = []

        for book in data['docs']:
            try:
                olid = book["edition_key"][-1]
                title = book["title"]
                author = book["author_name"]
                
                if "number_of_pages_median" in book:
                    number_of_pages = book["number_of_pages_median"]
                
                if "first_publish_year" in book:
                    publish_year = book["first_publish_year"]
                
                url = add_query_items(self.book_url, {"bibkeys": "OLID:" + str(olid)})
                response = requests.get(url, timeout=REQUESTS_TIMEOUT)

                book_details = json.loads(response.text)
                cover_url = book_details["OLID:" + str(olid)]["thumbnail_url"].replace('-S.jpg', '-M.jpg')

                entry = BookEntry(
                    olid=olid,
                    title=title,
                    author=author,
                    number_of_pages=number_of_pages,
                    publish_year=publish_year,
                    cover_url=cover_url
                )
                books.append(entry)
            except:
                pass

        return books

    def search_from_keywords(self, keywords):
        try:
            url = add_query_items(self.search_url, {"q": keywords})
            response = requests.get(url, timeout=REQUESTS_TIMEOUT)

            data = json.loads(response.text)
            books = self.get_books_info(data)
            return books
        except:
            print(traceback.format_exc())
            return []

    def search_from_title(self, title):
        try:
            url = add_query_items(self.search_url, {"title": title})
            response = requests.get(url, timeout=REQUESTS_TIMEOUT)

            data = json.loads(response.text)
            books = self.get_books_info(data)
            return books
        except:
            print(traceback.format_exc())
            return []

    def search_from_author(self, author):
        try:
            url = add_query_items(self.search_url, {"author": author})
            response = requests.get(url, timeout=REQUESTS_TIMEOUT)

            data = json.loads(response.text)
            books = self.get_books_info(data)
            return books
        except:
            print(traceback.format_exc())
            return []
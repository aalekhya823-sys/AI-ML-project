from abc import ABC, abstractmethod
from datetime import datetime



class User(ABC):
    def __init__(self, user_id: int, name: str):
        self._user_id = user_id
        self._name = name

    @abstractmethod
    def get_role(self):
        pass

    def get_details(self):
        return f"ID: {self._user_id}, Name: {self._name}, Role: {self.get_role()}"



class Student(User):
    def __init__(self, user_id: int, name: str):
        super().__init__(user_id, name)
        self.borrowed_books = []

    def get_role(self):
        return "Student"

    def borrow_book(self, book):
        if book.is_available():
            self.borrowed_books.append(book)
            book.borrow()
        else:
            raise Exception("Book is not available")


class Admin(User):
    def get_role(self):
        return "Admin"

    def add_book(self, library, book):
        library.add_book(book)


class Book:
    def __init__(self, isbn: str, title: str, author: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self._available = True

    def borrow(self):
        self._available = False

    def return_book(self):
        self._available = True

    def is_available(self):
        return self._available

    def __str__(self):
        status = "Available" if self._available else "Borrowed"
        return f"{self.title} by {self.author} [{status}]"


class Library:
    def __init__(self):
        self.books = []
        self.transactions = []

    def add_book(self, book: Book):
        self.books.append(book)

    def find_book(self, isbn: str):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def record_transaction(self, user, book, action):
        self.transactions.append({
            "user": user._name,
            "book": book.title,
            "action": action,
            "time": datetime.now()
        })



class LibraryService:
    def borrow_book(self, user: User, library: Library, isbn: str):
        book = library.find_book(isbn)
        if not book:
            raise Exception("Book not found")

        user.borrow_book(book)
        library.record_transaction(user, book, "BORROW")

    def return_book(self, user: Student, library: Library, isbn: str):
        book = library.find_book(isbn)
        
        print("Script is running successfully")


from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import datetime


@dataclass
class Book:
    title: str
    authors: List[str]
    edition: int

class Status(Enum):
    AVAILABLE = 1
    LOANED = 2
    LOST = 3

@dataclass
class BookItem:
    book: Book
    status: Status = Status.AVAILABLE
    date_borrowed: Optional[datetime.datetime] = None
    
    def checkout(self) -> bool:
        if self.status == Status.AVAILABLE:
            self.date_borrowed = datetime.datetime.now()
            self.status = Status.LOANED
            return True
        return False
    
    def return_book(self) -> bool:
        if self.status == Status.LOANED:
            self.status = Status.AVAILABLE
            self.date_borrowed = None
            return True
        return False

@dataclass
class Member:
    name: str
    member_id: int
    borrowed_books: List[BookItem] = field(default_factory=list)
    
    def borrow_book(self, book_item: BookItem) -> bool:
        if book_item.checkout():
            self.borrowed_books.append(book_item)
            return True
        return False
    
    def return_book(self, book_item: BookItem) -> bool:
        if book_item in self.borrowed_books and book_item.return_book():
            self.borrowed_books.remove(book_item)
            return True
        return False

@dataclass
class Library:
    items: List[BookItem]
    members: List[Member] = field(default_factory=list)
    
    def register_member(self, member: Member):
        self.members.append(member)
    
    def find_book_item(self, title: str) -> Optional[BookItem]:
        for item in self.items:
            if item.book.title == title and item.status == Status.AVAILABLE:
                return item
        return None

def main():
    # Create some books
    book1 = Book(title="The Great Gatsby", authors=["F. Scott Fitzgerald"], edition=1)
    book2 = Book(title="1984", authors=["George Orwell"], edition=1)
    
    # Create book items
    book_item1 = BookItem(book=book1)
    book_item2 = BookItem(book=book2)
    book_item3 = BookItem(book=book1)
    
    # Create a library and add book items
    library = Library(items=[book_item1, book_item2, book_item3])
    
    # Register a member
    member = Member(name="John Doe", member_id=1)
    library.register_member(member)
    
    # Member borrows a book
    book_to_borrow = library.find_book_item("The Great Gatsby")
    if book_to_borrow:
        print(f"Member borrowing '{book_to_borrow.book.title}': {member.borrow_book(book_to_borrow)}")
    
    # Member returns a book
    print(f"Member returning '{book_to_borrow.book.title}': {member.return_book(book_to_borrow)}")

if __name__ == "__main__":
    main()
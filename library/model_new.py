from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import datetime

LOAN_PERIOD_DAYS = 14  # Default loan period in days
COOLDOWN_DAYS = 7  # Days restricted from borrowing for a late return

# Custom exceptions with default messages
class LibraryError(Exception):
    """Base exception for library-related errors."""
    def __init__(self, message: str = "An error occurred in the library system"):
        super().__init__(message)

class NonMemberError(LibraryError):
    """Raised when an action is attempted by a non-member."""
    def __init__(self, member_name: str):
        message = f"{member_name} is not a registered member of the library."
        super().__init__(message)

class BookNotAvailableError(LibraryError):
    """Raised when a requested book is not available for checkout."""
    def __init__(self, book_title: str):
        message = f"The book '{book_title}' is currently not available for checkout."
        super().__init__(message)

class CooldownPeriodError(LibraryError):
    """Raised when a member is restricted from borrowing due to cooldown."""
    def __init__(self, member_name: str, cooldown_end_date: datetime.datetime):
        message = f"{member_name} is in a cooldown period until {cooldown_end_date}."
        super().__init__(message)

class ReturnError(LibraryError):
    """Raised when an error occurs during the return process."""
    def __init__(self, reason: str = "The book is either not loaned or was not borrowed by this member."):
        super().__init__(reason)

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
class Loan:
    book_item: 'BookItem'
    member: 'Member'
    date_borrowed: datetime.datetime
    date_returned: Optional[datetime.datetime] = None
    due_date: datetime.datetime = None

@dataclass
class BookItem:
    book: Book
    status: Status = Status.AVAILABLE

@dataclass
class Member:
    name: str
    cooldown_end_date: Optional[datetime.datetime] = None
    current_loan: Optional[BookItem] = None

@dataclass
class Library:
    items: List[BookItem] = field(default_factory=list)
    loan_history: List[Loan] = field(default_factory=list)
    members: List[Member] = field(default_factory=list)

    def add_book_item(self, book_item: BookItem):
        self.items.append(book_item)

    def add_member(self, member: Member):
        self.members.append(member)

    def checkout(self, book_item: BookItem, member: Member) -> None:
        if member not in self.members:
            raise NonMemberError(member.name)
        if member.cooldown_end_date and member.cooldown_end_date > datetime.datetime.now():
            raise CooldownPeriodError(member.name, member.cooldown_end_date)
        if book_item.status != Status.AVAILABLE:
            raise BookNotAvailableError(book_item.book.title)

        book_item.status = Status.LOANED
        date_borrowed = datetime.datetime.now()
        due_date = date_borrowed + datetime.timedelta(days=LOAN_PERIOD_DAYS)
        loan = Loan(book_item=book_item, member=member, date_borrowed=date_borrowed, due_date=due_date)
        member.current_loan = book_item
        self.loan_history.append(loan)

    def return_book(self, book_item: BookItem, member: Member) -> bool:
        if member not in self.members:
            raise NonMemberError(member.name)
        if book_item.status != Status.LOANED or member.current_loan != book_item:
            raise ReturnError()

        book_item.status = Status.AVAILABLE
        member.current_loan = None
        loan = next((loan for loan in self.loan_history if loan.book_item == book_item and loan.member == member and loan.date_returned is None), None)

        if loan:
            loan.date_returned = datetime.datetime.now()
            if loan.date_returned > loan.due_date:
                member.cooldown_end_date = datetime.datetime.now() + datetime.timedelta(days=COOLDOWN_DAYS)
                return False
        return True

def main():
    # Create books and book items
    book1 = Book(title="The Great Gatsby", authors=["F. Scott Fitzgerald"], edition=1)
    book_item1 = BookItem(book=book1)

    # Create a library and add book items
    library = Library()
    library.add_book_item(book_item1)

    # Create a member and add to the library
    member = Member(name="John Doe")
    library.add_member(member)

    # Member checks out a book
    try:
        library.checkout(book_item=book_item1, member=member)
        print(f"'{book_item1.book.title}' checked out successfully to '{member.name}'.")
        library.checkout(book_item=book_item1, member=member)  # Attempt to checkout again
    except LibraryError as e:
        print(f"Checkout error: {e}")

    # Simulate late return by manually setting status
    book_item1.status = Status.LOANED  # Manually set for testing

    # Member returns the book
    try:
        if library.return_book(book_item=book_item1, member=member):
            print(f"Book returned on time by '{member.name}'.")
        else:
            print(f"Book returned late! '{member.name}' is restricted from borrowing until {member.cooldown_end_date}.")
    except LibraryError as e:
        print(f"Return error: {e}")

if __name__ == '__main__':
    main()

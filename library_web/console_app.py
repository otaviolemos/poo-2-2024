from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from services import (
    add_book_to_library,
    list_all_books_with_items,
    borrow_book_item_by_id,
    return_book_item_by_id,
)

# UI Functions
def add_book_ui(session):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    copies = int(input("Enter the number of copies: "))
    book = add_book_to_library(session, title, author, copies)
    print(f"Book '{book.title}' by {book.author} with {copies} copies added to the library.")

def list_books_ui(session):
    books = list_all_books_with_items(session)
    if not books:
        print("No books in the library.")
    else:
        for book in books:
            print(f"Book ID {book.id}: {book.title} by {book.author}")
            for item in book.items:
                status = "Available" if item.is_available else "Borrowed"
                print(f"  Copy ID {item.id}: {status}")

def borrow_book_ui(session):
    item_id = int(input("Enter the ID of the book copy to borrow: "))
    item = borrow_book_item_by_id(session, item_id)
    if item:
        print(f"You have borrowed '{item.book.title}' (Copy ID {item.id}).")
    else:
        print("Book copy not found or already borrowed.")

def return_book_ui(session):
    item_id = int(input("Enter the ID of the book copy to return: "))
    item = return_book_item_by_id(session, item_id)
    if item:
        print(f"You have returned '{item.book.title}' (Copy ID {item.id}).")
    else:
        print("Book copy not found or was not borrowed.")

def add_book_item_ui(session):
    book_id = int(input("Enter the ID of the book to add a new copy: "))
    item = add_book_item(session, book_id)
    if item:
        print(f"New copy of '{item.book.title}' added with Copy ID {item.id}.")
    else:
        print("Book not found. Unable to add a new copy.")

def list_book_items_ui(session):
    book_id = int(input("Enter the ID of the book to list its copies: "))
    items = list_book_items(session, book_id)
    if items is None:
        print("Book not found.")
    elif not items:
        print("No copies available for this book.")
    else:
        print(f"Copies of '{items[0].book.title}' (Book ID {book_id}):")
        for item in items:
            status = "Available" if item.is_available else "Borrowed"
            print(f"  Copy ID {item.id}: {status}")

# Main loop
def main():
    session = Session()
    while True:
        print("\nLibrary Menu")
        print("1. Add Book")
        print("2. List Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Add Book Copy")
        print("6. List Book Copies")
        print("7. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_book_ui(session)
        elif choice == 2:
            list_books_ui(session)
        elif choice == 3:
            borrow_book_ui(session)
        elif choice == 4:
            return_book_ui(session)
        elif choice == 5:
            add_book_item_ui(session)
        elif choice == 6:
            list_book_items_ui(session)
        elif choice == 7:
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    DATABASE_URI = 'mysql+mysqlconnector://sql5747408:ZXr2RRDHxL@sql5.freemysqlhosting.net/sql5747408'
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    main()

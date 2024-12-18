from models import Base, BookItem, Book

def add_book_to_library(session, title, author, copies):
    book = Book(title=title, author=author)
    session.add(book)
    session.commit()
    for _ in range(copies):
        item = BookItem(book_id=book.id)
        session.add(item)
    session.commit()
    return book

def list_all_books_with_items(session):
    return session.query(Book).all()

def borrow_book_item_by_id(session, item_id):
    item = session.query(BookItem).get(item_id)
    if item and item.borrow():
        session.commit()
        return item
    return None

def return_book_item_by_id(session, item_id):
    item = session.query(BookItem).get(item_id)
    if item and item.return_item():
        session.commit()
        return item
    return None

def add_book_item(session, book_id):
    book = session.query(Book).get(book_id)
    if not book:
        return None
    new_item = BookItem(book_id=book_id)
    session.add(new_item)
    session.commit()
    return new_item

def list_book_items(session, book_id):
    book = session.query(Book).get(book_id)
    if not book:
        return None
    return book.items
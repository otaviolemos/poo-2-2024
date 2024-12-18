from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, BookItem, Book
from services import (
    add_book_to_library,
    list_all_books_with_items,
    borrow_book_item_by_id,
    return_book_item_by_id,
)

app = Flask(__name__)

# Database configuration
DATABASE_URI = 'mysql+mysqlconnector://sql5747408:ZXr2RRDHxL@sql5.freemysqlhosting.net/sql5747408'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Initialize database
def init_db():
    Base.metadata.create_all(engine)

init_db()

# Routes
@app.route("/books", methods=["GET"])
def get_books():
    session = Session()
    books = list_all_books_with_items(session)
    result = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "copies": [
                {
                    "id": item.id,
                    "is_available": item.is_available,
                }
                for item in book.items
            ],
        }
        for book in books
    ]
    session.close()
    return jsonify(result)

@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    title = data.get("title")
    author = data.get("author")
    copies = data.get("copies", 1)

    session = Session()
    try:
        book = add_book_to_library(session, title, author, copies)
        session.close()
        if not book:
            return jsonify({"error": "Failed to add book (duplicate or other error)."}), 400
        return jsonify({"message": f"Book '{title}' added with {copies} copies"}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Database integrity error occurred."}), 400

@app.route("/borrow/<int:item_id>", methods=["POST"])
def borrow_book(item_id):
    session = Session()
    item = borrow_book_item_by_id(session, item_id)
    session.close()
    if item:
        return jsonify({"message": f"Book copy {item_id} borrowed successfully"}), 200
    return jsonify({"error": "Book copy not found or already borrowed"}), 404

@app.route("/return/<int:item_id>", methods=["POST"])
def return_book(item_id):
    session = Session()
    item = return_book_item_by_id(session, item_id)
    session.close()
    if item:
        return jsonify({"message": f"Book copy {item_id} returned successfully"}), 200
    return jsonify({"error": "Book copy not found or not currently borrowed"}), 404

if __name__ == "__main__":
    app.run(debug=True)

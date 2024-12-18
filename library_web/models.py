from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)

    # One-to-Many relationship with BookItem
    items = relationship("BookItem", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author})>"

class BookItem(Base):
    __tablename__ = "book_items"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    is_available = Column(Boolean, default=True)

    # Relationship back to Book
    book = relationship("Book", back_populates="items")

    def borrow(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    def return_item(self):
        if not self.is_available:
            self.is_available = True
            return True
        return False

    def __repr__(self):
        return f"<BookItem(id={self.id}, is_available={self.is_available})>"


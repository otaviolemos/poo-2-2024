import React, { useEffect, useState } from "react";
import axios from "../api"

interface Book {
  id: number;
  title: string;
  author: string;
  copies: { id: number; is_available: boolean }[];
}

const ListBooks: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Fetch books when the component mounts
    console.log("Fetching books..."); // Debugging line
    axios
      .get("/books")
      .then((response) => {
        console.log("Books fetched:", response.data); // Debugging line
        setBooks(response.data);
        setLoading(false); // Set loading to false once the books are fetched
      })
      .catch((error) => {
        console.error("Error fetching books:", error);
        setLoading(false); // Stop loading even if there's an error
      });
  }, []);

  if (loading) {
    return <p>Loading books...</p>; // Show loading message while fetching
  }

  return (
    <div>
      <h2>List of Books</h2>
      {books.length === 0 ? (
        <p>No books available</p>
      ) : (
        <ul>
          {books.map((book) => (
            <li key={book.id}>
              {book.title} by {book.author}
              <ul>
                {book.copies.map((copy) => (
                  <li key={copy.id}>
                    Copy ID: {copy.id}, Status: {copy.is_available ? "Available" : "Borrowed"}
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ListBooks;

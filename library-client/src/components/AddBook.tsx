import React, { useState } from "react";
import { addBook } from "../services/api";

const AddBook: React.FC = () => {
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const [copies, setCopies] = useState(1);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        try {
            const response = await addBook(title, author, copies);
            alert(response.data.message);
            setTitle("");
            setAuthor("");
            setCopies(1);
            window.location.reload(); // Reload the page
        } catch (error) {
            alert("Error adding book.");
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Add Book</h2>
            <div>
                <label>Title:</label>
                <input value={title} onChange={(e) => setTitle(e.target.value)} />
            </div>
            <div>
                <label>Author:</label>
                <input value={author} onChange={(e) => setAuthor(e.target.value)} />
            </div>
            <div>
                <label>Copies:</label>
                <input
                    type="number"
                    value={copies}
                    onChange={(e) => setCopies(Number(e.target.value))}
                />
            </div>
            <button type="submit">Add Book</button>
        </form>
    );
};

export default AddBook;

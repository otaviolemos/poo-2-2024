import React, { useState } from "react";
import { returnBook } from "../services/api";

const ReturnBook: React.FC = () => {
    const [itemId, setItemId] = useState("");

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        try {
            const response = await returnBook(Number(itemId));
            alert(response.data.message);
            setItemId("");
        } catch (error) {
            alert("Error returning book.");
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Return Book</h2>
            <div>
                <label>Copy ID:</label>
                <input
                    value={itemId}
                    onChange={(e) => setItemId(e.target.value)}
                />
            </div>
            <button type="submit">Return</button>
        </form>
    );
};

export default ReturnBook;

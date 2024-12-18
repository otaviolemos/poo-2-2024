import React, { useState } from "react";
import { borrowBook } from "../services/api";

const BorrowBook: React.FC = () => {
    const [itemId, setItemId] = useState("");

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        try {
            const response = await borrowBook(Number(itemId));
            alert(response.data.message);
            setItemId("");
        } catch (error) {
            alert("Error borrowing book.");
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Borrow Book</h2>
            <div>
                <label>Copy ID:</label>
                <input
                    value={itemId}
                    onChange={(e) => setItemId(e.target.value)}
                />
            </div>
            <button type="submit">Borrow</button>
        </form>
    );
};

export default BorrowBook;

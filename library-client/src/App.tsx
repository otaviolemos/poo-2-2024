import React from "react";
import AddBook from "./components/AddBook";
import ListBooks from "./components/ListBooks";
import BorrowBook from "./components/BorrowBook";
import ReturnBook from "./components/ReturnBook";

const App: React.FC = () => {
    return (
        <div>
            <h1>Library Management</h1>
            <AddBook />
            <hr />
            <ListBooks />
            <hr />
            <BorrowBook />
            <hr />
            <ReturnBook />
        </div>
    );
};

export default App;

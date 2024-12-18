import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

export const getBooks = () => axios.get(`${API_BASE_URL}/books`);

export const addBook = (title: string, author: string, copies: number) =>
    axios.post(`${API_BASE_URL}/books`, { title, author, copies });

export const borrowBook = (itemId: number) =>
    axios.post(`${API_BASE_URL}/borrow/${itemId}`);

export const returnBook = (itemId: number) =>
    axios.post(`${API_BASE_URL}/return/${itemId}`);

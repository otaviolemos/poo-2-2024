import axios from "axios";

// Create an instance of Axios with the base URL of the Flask backend
const api = axios.create({
  baseURL: "http://localhost:5000", // Update this URL with your Flask backend URL
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
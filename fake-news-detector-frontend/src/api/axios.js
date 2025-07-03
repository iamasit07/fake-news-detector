import axios from 'axios';

export const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000', // Change if your backend runs on a different port
  headers: {
    'Content-Type': 'application/json',
  },
});

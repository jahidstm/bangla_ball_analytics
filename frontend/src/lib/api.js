import axios from 'axios';

// Base API instance
export const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true, // important for cookies (PIN auth)
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If 401 Unauthorized, maybe redirect to login
    if (error.response?.status === 401 && typeof window !== 'undefined') {
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

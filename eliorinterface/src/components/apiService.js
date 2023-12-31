// apiService.js
import axios from 'axios';

// Base URL for the API
const API_BASE_URL = 'http://apihost:5001/api';

// Function to query the view
export const queryView = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/query_view`);
    return response.data;
  } catch (error) {
    console.error('Error fetching data from the API', error);
    throw error;
  }
};

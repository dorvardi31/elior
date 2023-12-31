import axios from 'axios';

const API_BASE_URL = 'http://apihost:5001/api/';

export function fetchData(query) {
  return axios.get(`${API_BASE_URL}query_view`, {
    params: { search: query }
  });
}

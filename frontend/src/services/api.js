import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds
});

export const generatePost = async (data, endpoint = 'standard') => {
  const url = endpoint === 'enhanced' 
    ? '/api/v1/generate-post-enhanced' 
    : '/api/v1/generate-post';
  
  const response = await api.post(url, data);
  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get('/api/v1/health');
  return response.data;
};

export default api;
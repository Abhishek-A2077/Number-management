import axios from 'axios';

const API_BASE = 'http://20.244.56.144/test';
let ACCESS_TOKEN = 'SUfGJv';

export const fetchNumbers = async (type) => {
  try {
    const response = await axios.get(`${API_BASE}/${type}`, {
      headers: { Authorization: `Bearer ${ACCESS_TOKEN}` }
    });
    return response.data.numbers;
  } catch (error) {
    console.error('API Error:', error);
    return [];
  }
};

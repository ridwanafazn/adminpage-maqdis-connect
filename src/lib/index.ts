import axios from 'axios';

// Ambil baseURL dari environment variable
const baseURL = import.meta.env.VITE_BASE_URL;

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Fungsi login
export const login = async (email: string, password: string) => {
  try {
    const response = await api.post('/api/auth/login', { email, password });
    return response.data;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};

// Fungsi untuk mengambil daftar grup
export const getGroups = async (token: string) => {
  try {
    const response = await api.get('/api/Group', {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch groups:', error);
    throw error;
  }
};

// Fungsi untuk mengambil daftar room
export const getRooms = async (token: string) => {
  try {
    const response = await api.get('/api/Audio/getRoom', {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch rooms:', error);
    throw error;
  }
};

// Fungsi untuk membuat grup baru
export const createGroup = async (userId: string, token: string) => {
  try {
    // Membuat grup
    const groupResponse = await api.post(`/api/Group/admin?userId=${userId}`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Membuat room dengan nama grup yang sama
    const roomResponse = await api.post('/api/Audio/generateToken', {
      nama_room: groupResponse.data.nama_grup,
    }, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Assign room ke grup
    const assignResponse = await api.post('/api/Audio/assignRoom', {
      roomid: roomResponse.data.room.id,
      grupid: groupResponse.data.grupid,
    }, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Refresh token
    const refreshTokenResponse = await api.post('/api/Audio/refreshToken', {
      room_Id: roomResponse.data.room.id,
    }, {
      headers: { Authorization: `Bearer ${token}` },
    });

    return { groupResponse, roomResponse, assignResponse, refreshTokenResponse };
  } catch (error) {
    console.error('Error during group creation:', error);
    throw error;
  }
};
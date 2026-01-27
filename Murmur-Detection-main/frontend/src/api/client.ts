import axios from 'axios';

const apiBase = import.meta.env.VITE_API_URL;

export const api = axios.create({
  baseURL: apiBase
});

export const getHealth = () => api.get('/api/health');

export const predictMurmur = (formData: FormData) =>
  api.post('/api/predict', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

export const fetchHistory = (patientId?: string) =>
  api.get('/api/history', { params: { patient_id: patientId } });

export const fetchHistoryDetail = (requestId: string) => api.get(`/api/history/${requestId}`);

export const deleteHistory = (requestId: string) => api.delete(`/api/history/${requestId}`);

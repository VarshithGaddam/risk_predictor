import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.MODE === 'production' 
    ? 'https://risk-predictor-1.onrender.com' 
    : 'http://localhost:5000'
)

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const dashboardAPI = {
  getMetrics: () => api.get('/api/dashboard/metrics'),
  getRiskDistribution: () => api.get('/api/dashboard/risk-distribution')
}

export const patientsAPI = {
  getAll: (params) => api.get('/api/patients', { params }),
  getById: (id) => api.get(`/api/patients/${id}`),
  uploadCSV: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/data/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  loadDemo: () => api.post('/api/data/load-demo'),
  deletePatient: (id) => api.delete(`/api/patients/${id}`),
  clearAll: () => api.delete('/api/data/clear-all')
}

export const predictAPI = {
  predictRisk: (patientId) => api.post('/api/predict/risk', { patientId })
}

export const notesAPI = {
  analyze: (noteText) => api.post('/api/notes/analyze', { noteText })
}

export default api

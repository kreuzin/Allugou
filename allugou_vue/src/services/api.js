import axios from 'axios'

const API_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000
})

export const getMediaUrl = (path) => {
  if (!path) return null
  if (path.startsWith('http')) return path
  return `${API_URL}${path}`
}

export const ofertaLocacaoService = {
  async getAllOfertas() {
    try {
      console.log('Making request to:', `${api.defaults.baseURL}/ofsloc/`)
      const response = await api.get('/ofsloc/')
      console.log('API Status:', response.status)
      console.log('API Headers:', response.headers)
      console.log('API Data:', response.data)
      return response
    } catch (error) {
      console.error('API Error Details:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      })
      throw error
    }
  },
  
  getOfertaById(id) {
    return api.get(`/ofsloc/${id}/`)
  },
  
  getImagensOferta(ofertaId) {
    return api.get(`/imagens-oferta/?oferta=${ofertaId}`)
  }
}

export default api
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
      const response = await api.get('/api/ofertas/all/')
      return response
    } catch (error) {
      console.error('erro ao buscar ofertas:', error)
      throw error
    }
  },
  
  getOfertaById(id) {
    return api.get(`/api/ofertas/${id}/`)
  },
  
  getImagensOferta(ofertaId) {
    return api.get(`/imagens-oferta/?oferta=${ofertaId}`)
  }
}

export default api
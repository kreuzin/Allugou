import axios from 'axios'

// pega a url da api das variaveis de ambiente ou usa localhost como padrao
const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
  withCredentials: true,
  headers: {
    'ngrok-skip-browser-warning': 'true'
  }
})

export const getMediaUrl = (path) => {
  if (!path) return null
  // se ja é url completa, retorna direto
  if (path.startsWith('http')) return path
  // garante que o path começa com /
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  const url = `${API_URL}${normalizedPath}`
  console.log('getMediaUrl:', { path, API_URL, url })  // debug temporario
  return url
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
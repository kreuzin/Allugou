import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
})

// inicializar token csrf
async function initializeCSRF() {
    try {
        const response = await api.get('/api/csrf/')
        const csrfToken = response.data.csrfToken
        // definir o token nos headers padrão
        api.defaults.headers.common['X-CSRFToken'] = csrfToken
        return csrfToken
    } catch (error) {
        console.error('Falha ao buscar token csrf:', error)
    }
}

// inicializar token csrf quando o módulo é importado
initializeCSRF()

// adicionar interceptador de resposta para tratamento de erros
api.interceptors.response.use(
    response => response,
    error => {
        // se receber um erro 403 e não tiver reintentado, tente atualizar o token csrf
        if (error.response?.status === 403 && !error.config._retry) {
            error.config._retry = true
            return initializeCSRF().then(() => api(error.config))
        }
        return Promise.reject(error)
    }
)

export default api;
import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
})

// pega cookie pelo nome
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^|; )' + name + '=([^;]+)'))
    return match ? decodeURIComponent(match[2]) : null
}

// busca o token csrf se precisar
async function initializeCSRF() {
    try {
        const response = await api.get('/api/csrf/')
        const csrfToken = response.data.csrfToken
        return csrfToken
    } catch (error) {
        console.error('Falha ao buscar token csrf:', error)
    }
}

// antes de cada request: joga o csrf no header
api.interceptors.request.use(config => {
    try {
        const csrftoken = getCookie('csrftoken')
        if (csrftoken) {
            config.headers['X-CSRFToken'] = csrftoken
        }
    } catch (e) {
        // silencioso
    }
    return config
})

// trata erros de resposta
api.interceptors.response.use(
    response => response,
    error => {
        // se der 403 e nao tentou ainda, atualiza csrf e tenta de novo
        if (error.response?.status === 403 && !error.config._retry) {
            error.config._retry = true
            // pega token novo e manda de novo
            return initializeCSRF().then(() => api(error.config))
        }
        return Promise.reject(error)
    }
)

export default api;
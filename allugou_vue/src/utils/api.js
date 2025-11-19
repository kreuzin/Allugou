import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
})

// util para ler cookie pelo nome
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^|; )' + name + '=([^;]+)'))
    return match ? decodeURIComponent(match[2]) : null
}

// inicializar token csrf se necessário (chamada explícita)
async function initializeCSRF() {
    try {
        const response = await api.get('/api/csrf/')
        const csrfToken = response.data.csrfToken
        return csrfToken
    } catch (error) {
        console.error('Falha ao buscar token csrf:', error)
    }
}

// interceptador de requisição: sempre define header x-csrftoken com o cookie atual
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

// adicionar interceptador de resposta para tratamento de erros
api.interceptors.response.use(
    response => response,
    error => {
        // se receber um erro 403 e não tiver reintentado, tente atualizar o token csrf
        if (error.response?.status === 403 && !error.config._retry) {
            error.config._retry = true
            // buscar novo token e tentar novamente
            return initializeCSRF().then(() => api(error.config))
        }
        return Promise.reject(error)
    }
)

export default api;
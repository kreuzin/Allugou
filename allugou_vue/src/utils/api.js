import axios from 'axios'

// pega a url da api das variaveis de ambiente ou usa localhost como padrao
// em producao a VUE_APP_API_URL vai ser a url do ngrok
const apiUrl = process.env.VUE_APP_API_URL || 'http://localhost:8000'

// guarda o token csrf em memoria pra usar nas requisicoes
let csrfToken = null

const api = axios.create({
    baseURL: apiUrl,
    withCredentials: true,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    headers: {
        'ngrok-skip-browser-warning': 'true'  // pula a pagina de aviso do ngrok
    }
})

// pega cookie pelo nome
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^|; )' + name + '=([^;]+)'))
    return match ? decodeURIComponent(match[2]) : null
}

// busca o token csrf do servidor e guarda em memoria
async function initializeCSRF() {
    try {
        const response = await api.get('/api/csrf/')
        csrfToken = response.data.csrfToken
        return csrfToken
    } catch (error) {
        console.error('Falha ao buscar token csrf:', error)
    }
}

// antes de cada request: joga o csrf no header
api.interceptors.request.use(config => {
    // primeiro tenta pegar do cookie, se nao tiver usa o que ta em memoria
    const token = getCookie('csrftoken') || csrfToken
    if (token) {
        config.headers['X-CSRFToken'] = token
    }
    return config
})

// trata erros de resposta
api.interceptors.response.use(
    response => response,
    async error => {
        // se der 403 e nao tentou ainda, atualiza csrf e tenta de novo
        if (error.response?.status === 403 && !error.config._retry) {
            error.config._retry = true
            // pega token novo e manda de novo
            await initializeCSRF()
            error.config.headers['X-CSRFToken'] = csrfToken
            return api(error.config)
        }
        return Promise.reject(error)
    }
)

export { initializeCSRF }
export default api;
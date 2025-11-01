import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
})

// Initialize CSRF token
async function initializeCSRF() {
    try {
        await api.get('/api/csrf/')
    } catch (error) {
        console.error('Failed to fetch CSRF token:', error)
    }
}

// Initialize CSRF token when the module is imported
initializeCSRF()

// Add response interceptor for error handling
api.interceptors.response.use(
    response => response,
    error => {
        // If we get a 403 error and we haven't retried yet, try to refresh the CSRF token
        if (error.response?.status === 403 && !error.config._retry) {
            error.config._retry = true
            return initializeCSRF().then(() => api(error.config))
        }
        return Promise.reject(error)
    }
)

export default api;
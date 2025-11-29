import api from '@/utils/api'

// restaura estado do localStorage se existir
const savedAuth = localStorage.getItem('auth')
const initialState = savedAuth ? JSON.parse(savedAuth) : {
    isAuthenticated: false,
    user: null,
    userType: null,
    error: null
}

const state = {
    isAuthenticated: initialState.isAuthenticated,
    user: initialState.user,
    userType: initialState.userType,
    error: null
}

const getters = {
    isAuthenticated: state => state.isAuthenticated,
    user: state => state.user,
    userType: state => state.userType,
    isLocador: state => state.userType === 'locador',
    error: state => state.error
}

// salva estado no localStorage
function saveToStorage(state) {
    localStorage.setItem('auth', JSON.stringify({
        isAuthenticated: state.isAuthenticated,
        user: state.user,
        userType: state.userType
    }))
}

const actions = {
    async login({ commit, state }, credentials) {
        try {
            const response = await api.post('/api/login/', credentials)
            if (response.data.success) {
                commit('setUser', response.data.user)
                commit('setUserType', response.data.user_type)
                commit('setAuthenticated', true)
                commit('setError', null)
                saveToStorage(state)
                return true
            } else {
                commit('setError', response.data.message || 'Falha no login')
                return false
            }
        } catch (error) {
            commit('setError', error.response?.data?.message || 'Erro de conexão')
            return false
        }
    },

    async logout({ commit }) {
        try {
            await api.post('/api/logout/')
        } catch (error) {
            // ignora erro de logout
        }
        commit('setUser', null)
        commit('setUserType', null)
        commit('setAuthenticated', false)
        commit('setError', null)
        localStorage.removeItem('auth')
    },

    // verifica se a sessão ainda é válida no backend
    async checkSession({ commit, state }) {
        if (!state.isAuthenticated) return false
        
        try {
            const response = await api.get('/api/check-session/')
            if (response.data.success && response.data.authenticated) {
                // sessão válida, atualiza dados se necessário
                commit('setUser', response.data.user)
                commit('setUserType', response.data.user_type)
                saveToStorage(state)
                return true
            } else {
                // sessão expirou no backend
                commit('setUser', null)
                commit('setUserType', null)
                commit('setAuthenticated', false)
                localStorage.removeItem('auth')
                return false
            }
        } catch (error) {
            // erro de conexão, mantém estado local
            return state.isAuthenticated
        }
    },

    clearError({ commit }) {
        commit('setError', null)
    }
}

const mutations = {
    setUser(state, user) {
        state.user = user
    },
    setUserType(state, userType) {
        state.userType = userType
    },
    setAuthenticated(state, isAuthenticated) {
        state.isAuthenticated = isAuthenticated
    },
    setError(state, error) {
        state.error = error
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
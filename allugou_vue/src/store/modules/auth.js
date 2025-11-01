import api from '@/utils/api'

const state = {
    isAuthenticated: false,
    user: null,
    error: null
}

const getters = {
    isAuthenticated: state => state.isAuthenticated,
    user: state => state.user,
    error: state => state.error
}

const actions = {
    async login({ commit }, credentials) {
        try {
            const response = await api.post('/api/login/', credentials)
            if (response.data.success) {
                commit('setUser', response.data.user)
                commit('setAuthenticated', true)
                commit('setError', null)
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
            commit('setUser', null)
            commit('setAuthenticated', false)
            commit('setError', null)
        } catch (error) {
            commit('setError', 'Falha ao sair')
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
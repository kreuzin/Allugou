import api from '@/utils/api'

const state = {
    requisicoes: [],
    mensagens: [],
    naoLidas: 0,
    mensagensNaoLidas: 0,
    loading: false,      // só true no primeiro carregamento
    initialized: false,  // indica se já carregou pelo menos uma vez
    error: null
}

const getters = {
    requisicoes: state => state.requisicoes,
    mensagens: state => state.mensagens,
    naoLidas: state => state.naoLidas,
    mensagensNaoLidas: state => state.mensagensNaoLidas,
    totalNaoLidas: state => state.naoLidas + state.mensagensNaoLidas,
    loading: state => state.loading,
    hasNotifications: state => (state.naoLidas + state.mensagensNaoLidas) > 0
}

const actions = {
    async fetchNotificacoesLocador({ commit, state }) {
        // so mostra loading se ainda não inicializou (primeiro carregamento)
        if (!state.initialized) {
            commit('setLoading', true)
        }
        try {
            const response = await api.get('/api/notificacoes/locador/')
            if (response.data.success) {
                commit('setRequisicoes', response.data.requisicoes)
                commit('setMensagens', response.data.mensagens || [])
                commit('setNaoLidas', response.data.naoLidas)
                commit('setMensagensNaoLidas', response.data.mensagensNaoLidas || 0)
            }
            commit('setError', null)
            commit('setInitialized', true)
        } catch (error) {
            commit('setError', error.response?.data?.message || 'Erro ao carregar notificações')
        } finally {
            commit('setLoading', false)
        }
    },

    async fetchNotificacoesLocatario({ commit, state }) {
        // so mostra loading se ainda não inicializou (primeiro carregamento)
        if (!state.initialized) {
            commit('setLoading', true)
        }
        try {
            const response = await api.get('/api/notificacoes/locatario/')
            if (response.data.success) {
                commit('setRequisicoes', response.data.requisicoes)
                commit('setMensagens', response.data.mensagens || [])
                commit('setNaoLidas', 0)
                commit('setMensagensNaoLidas', response.data.mensagensNaoLidas || 0)
            }
            commit('setError', null)
            commit('setInitialized', true)
        } catch (error) {
            commit('setError', error.response?.data?.message || 'Erro ao carregar requisições')
        } finally {
            commit('setLoading', false)
        }
    },

    async marcarVista({ commit, state }, requisicaoId) {
        try {
            await api.post(`/api/requisicoes/${requisicaoId}/marcar-vista/`)
            // atualiza localmente
            commit('marcarRequisicaoVista', requisicaoId)
        } catch (error) {
            console.error('Erro ao marcar requisição como vista:', error)
        }
    },

    clearNotifications({ commit }) {
        commit('setRequisicoes', [])
        commit('setMensagens', [])
        commit('setNaoLidas', 0)
        commit('setMensagensNaoLidas', 0)
        commit('setInitialized', false)
    }
}

const mutations = {
    setRequisicoes(state, requisicoes) {
        state.requisicoes = requisicoes
    },
    setMensagens(state, mensagens) {
        state.mensagens = mensagens
    },
    setNaoLidas(state, count) {
        state.naoLidas = count
    },
    setMensagensNaoLidas(state, count) {
        state.mensagensNaoLidas = count
    },
    setLoading(state, loading) {
        state.loading = loading
    },
    setError(state, error) {
        state.error = error
    },
    setInitialized(state, initialized) {
        state.initialized = initialized
    },
    marcarRequisicaoVista(state, requisicaoId) {
        const req = state.requisicoes.find(r => r.id === requisicaoId)
        if (req && !req.vistoPeloLocador) {
            req.vistoPeloLocador = true
            state.naoLidas = Math.max(0, state.naoLidas - 1)
        }
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}

<template>
  <div class="container" style="max-width: 520px; margin: 2rem auto;">
    <h2>Recuperar senha</h2>
    <p>Informe o e-mail associado à sua conta. Enviaremos instruções para redefinir sua senha.</p>

    <div v-if="success" class="alert alert-success">{{ success }}</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label class="form-label">E-mail</label>
        <input v-model="email" type="email" class="form-control" required />
      </div>

      <button :disabled="loading" class="btn btn-primary">
        {{ loading ? 'Enviando...' : 'Enviar instruções' }}
      </button>
      <router-link to="/login" class="btn btn-link ms-2">Voltar ao login</router-link>
    </form>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'ForgotPasswordView',
  data() {
    return {
      email: '',
      loading: false,
      success: null,
      error: null
    }
  },
  methods: {
    async handleSubmit() {
      this.error = null
      this.success = null
      this.loading = true
      try {
        const resp = await api.post('/api/password-reset/', { email: this.email })
        if (resp.data && resp.data.success) {
          this.success = resp.data.message || 'Instruções enviadas para o seu e-mail.'
        } else {
          this.error = resp.data?.message || 'Falha ao solicitar recuperação de senha.'
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Erro de conexão ao solicitar recuperação.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.container { padding: 1rem; }
</style>

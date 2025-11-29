<template>
  <div class="login-form">
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    <form @submit.prevent="handleSubmit">
      <div class="form-group mb-3">
        <label for="username" class="form-label">Nome de usuário</label>
        <input
          type="text"
          class="form-control"
          id="username"
          v-model="username"
          required
        />
      </div>
      <div class="form-group mb-3">
        <label for="password" class="form-label">Senha</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="password"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Entrar</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  computed: {
    error() {
      return this.$store.getters['auth/error']
    }
  },
  methods: {
    async handleSubmit() {
      const success = await this.$store.dispatch('auth/login', {
        username: this.username,
        password: this.password
      })

      if (success) {
        // isso aq é pra redirecionar pra pagina que o user tentou acessar antes de logar
        const redirect = this.$route.query.redirect || '/'
        // so redireciona se n tiver na mesma pagina
        if (this.$route.path !== redirect) {
          this.$router.push(redirect).catch(() => {})
        }
      }
    }
  }
}
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
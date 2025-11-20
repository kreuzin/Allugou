<template>
  <div class="login-view">
    <h2 class="text-center mb-4">Entrar</h2>
    <LoginForm />
    <div class="text-center mt-3">
      <router-link to="/register">Não tem uma conta? Cadastre-se aqui</router-link>
      <div class="mt-2">
        <router-link to="/forgot-password">Esqueci minha senha</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue'

export default {
  name: 'LoginView',
  components: {
    LoginForm
  }
}
</script>
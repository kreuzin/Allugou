<template>
  <div class="register-view">
    <h2 class="text-center mb-4">Criar conta</h2>
    <RegisterForm />
    <div class="text-center mt-3">
      <router-link to="/login">Já tem uma conta? Entre aqui</router-link>
    </div>
  </div>
</template>

<script>
import RegisterForm from '@/components/RegisterForm.vue'

export default {
  name: 'RegisterView',
  components: {
    RegisterForm
  }
}
</script>
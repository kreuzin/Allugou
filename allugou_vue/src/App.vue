<template>
  <div id="wrapper">
    <nav class="navbar navbar-dark">
      <div class="container d-flex align-items-center py-2">
        <router-link to="/" class="navbar-brand me-4">
          <span class="brand-text"><strong>All</strong>ugou</span>
        </router-link>
        
        <template v-if="!isAuthPage">
          <form class="search-form flex-grow-1 me-4">
            <div class="input-group">
              <input 
                type="search" 
                class="form-control search-input" 
                placeholder="Do que está precisando?"
                aria-label="Buscar"
              />
              <button class="btn search-button" type="submit">
                <i class="fa fa-search"></i>
              </button>
            </div>
          </form>

          <div class="notifications me-4">
            <button class="btn btn-icon">
              <i class="fa-solid fa-bell"></i>
            </button>
          </div>
        </template>
        

        <!-- se nao for a pagina do login mostra funções extras -->
        <div class="nav-buttons d-flex gap-2 align-items-center" v-if="!isAuthPage">
          <template v-if="isAuthenticated">
            <router-link to="/ads" class="btn btn-outline-light">
              <i class="fa-regular fa-rectangle-list me-1"></i>
              Seus anúncios
            </router-link>
            <router-link to="/new-ad" class="btn btn-danger">Anuncie agora!</router-link>
            <div class="d-flex align-items-center ms-2 me-2 text-white">
              <i class="fa-regular fa-user me-1"></i>
              <span>{{ user?.nome || user?.username }}</span>
            </div>
            <button @click="handleLogout" class="btn btn-outline-light">Sair</button>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-outline-light">Entrar</router-link>
          </template>
        </div>
      </div>
    </nav>

    <section class="text-center py-5">    <!--padding top e  bottom 5-->
      <router-view/>  <!--Welcome message do vue-->
    </section>


    <footer class="bg-dark text-white py-4 mt-auto">
      <p class="text-center">Copyright (c) 2025</p>
    </footer>

  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'



export default {
  name: 'App',
  computed: {
    // página de autenticação (login / register)
    isAuthPage() {
      return this.$route.path === '/login' || this.$route.path === '/register'
    },

    // estado reativo vindo do vuex
    isAuthenticated() {
      return this.$store.getters['auth/isAuthenticated']
    },

    // usuário atual vindo do vuex
    user() {
      return this.$store.getters['auth/user']
    }
  },
  methods: {
    async handleLogout() {
      await this.$store.dispatch('auth/logout')
      // usar replace e suprimir erros de redirecionamento concorrente
      this.$router.replace('/login').catch(() => {})
    }
  }
}
</script>

<style lang="scss">
.navbar {
  background: linear-gradient(to right, #00251a, #004d40);
  padding: 0.75rem 0;
}

.navbar-brand {
  padding: 0;
  margin: 0;
}

.brand-text {
  font-size: 1.75rem;
  color: white;
  letter-spacing: -0.5px;
}

.search-form {
  max-width: 600px;
}

.input-group {
  border-radius: 50px;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.search-input {
  background: transparent !important;
  border: none;
  color: white !important;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  border-color: transparent !important;
}

.search-input::placeholder {
  color: rgb(255, 255, 255, 0.7) !important;
  font-weight: 500;
}

.search-input:focus {
  box-shadow: none;
  background: rgba(255, 255, 255, 0.1) !important;
  outline: none;
  border-color: transparent;
}

.search-input:focus-visible {
  outline: none;
}

/* remover anel de foco padrão para todos os controles de formulário na barra de navegação */
.navbar .form-control:focus {
  outline: none;
  box-shadow: none;
  border-color: transparent;
}

.search-button {
  background: transparent;
  border: none;
  color: #ffffff;
  padding: 0 1.5rem;
  font-size: 1.1rem;
}

.search-button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.search-button i {
  color: #ffffff;
}

.btn-icon {
  color: #ffffff;
  font-size: 1.8rem;
  padding: 0.5rem;
  line-height: 1;
}

.btn-icon:hover {
  color: #ffffff;
}

.notifications .btn-icon {
  font-size: 2rem;
  padding: 0.25rem;
}

/* fazer todos os ícones da barra de navegação branco */
.navbar i {
  color: #ffffff !important;
}

.nav-buttons .btn {
  padding: 0.5rem 1rem;
  font-weight: 500;
  border-radius: 4px;
}

.btn-outline-light {
  border-color: rgba(255, 255, 255, 0.3);
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-danger {
  background-color: #f44336;
  border: none;
}

.btn-danger:hover {
  background-color: #d32f2f;
}

@media (max-width: 992px) {
  .nav-buttons {
    display: none !important;
  }
  
  .notifications {
    margin-right: 0 !important;
  }
}
</style>

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

          <div class="notifications me-4" v-if="isAuthenticated">
            <div class="dropdown">
              <button 
                class="btn btn-icon" 
                @click="toggleNotifications"
                ref="notificationBtn"
              >
                <i class="fa-solid fa-bell"></i>
                <span 
                  v-if="totalNaoLidas > 0" 
                  class="notification-badge"
                >
                  {{ totalNaoLidas > 9 ? '9+' : totalNaoLidas }}
                </span>
              </button>
              
              <transition name="dropdown">
                <div 
                  v-if="showNotifications" 
                  class="dropdown-menu dropdown-menu-end notification-dropdown show"
                  @click.stop
                >
                <div class="dropdown-header d-flex justify-content-between align-items-center">
                  <span>Notificações</span>
                  <div>
                    <span v-if="naoLidas > 0" class="badge bg-primary me-1">{{ naoLidas }} req</span>
                    <span v-if="mensagensNaoLidas > 0" class="badge bg-info">{{ mensagensNaoLidas }} msg</span>
                  </div>
                </div>
                
                <div v-if="loadingNotifications" class="text-center py-3">
                  <div class="spinner-border spinner-border-sm text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                  </div>
                </div>
                
                <div v-else-if="requisicoes.length === 0 && mensagens.length === 0" class="text-center py-3 text-muted">
                  <i class="fa-regular fa-bell-slash mb-2 d-block"></i>
                  Nenhuma notificação
                </div>
                
                <div v-else class="notification-list">
                  <!-- mensagens não lidas -->
                  <router-link 
                    v-for="msg in mensagens.slice(0, 3)" 
                    :key="'msg-' + msg.id"
                    :to="getMensagemLink(msg)"
                    class="dropdown-item notification-item unread"
                    @click.native="closeNotifications"
                  >
                    <div class="d-flex align-items-center">
                      <img 
                        v-if="msg.oferta.imagemPrincipal" 
                        :src="getImageUrl(msg.oferta.imagemPrincipal)" 
                        class="notification-image me-2"
                        alt="oferta"
                      >
                      <div v-else class="notification-image-placeholder me-2">
                        <i class="fa-solid fa-comment"></i>
                      </div>
                      <div class="notification-content">
                        <div class="notification-title">
                          <i class="fa-solid fa-comment text-info me-1"></i>
                          Nova mensagem
                        </div>
                        <div class="notification-text">{{ msg.texto }}</div>
                        <div class="notification-meta">
                          <span>{{ msg.remetenteNome }}</span>
                          <span class="ms-2 text-muted">{{ formatDate(msg.enviadoEm) }}</span>
                        </div>
                      </div>
                      <span class="unread-dot"></span>
                    </div>
                  </router-link>
                  
                  <!-- requisições -->
                  <router-link 
                    v-for="req in requisicoes.slice(0, 5 - Math.min(mensagens.length, 3))" 
                    :key="'req-' + req.id"
                    :to="`/requisicao/${req.id}`"
                    class="dropdown-item notification-item"
                    :class="{ 'unread': !req.vistoPeloLocador && isLocador }"
                    @click.native="closeNotifications"
                  >
                    <div class="d-flex align-items-center">
                      <img 
                        v-if="req.oferta.imagemPrincipal" 
                        :src="getImageUrl(req.oferta.imagemPrincipal)" 
                        class="notification-image me-2"
                        alt="oferta"
                      >
                      <div class="notification-content">
                        <div class="notification-title">
                          <span v-if="isLocador">Nova solicitação</span>
                          <span v-else>Sua requisição</span>
                        </div>
                        <div class="notification-text">{{ req.oferta.titulo }}</div>
                        <div class="notification-meta">
                          <span v-if="isLocador">{{ req.locatario.nome }}</span>
                          <span v-else class="badge" :class="statusBadgeClass(req.status)">{{ req.status }}</span>
                          <span class="ms-2 text-muted">{{ formatDate(req.dataCriacao) }}</span>
                        </div>
                      </div>
                      <span v-if="!req.vistoPeloLocador && isLocador" class="unread-dot"></span>
                    </div>
                  </router-link>
                </div>
                
                <div v-if="requisicoes.length > 5" class="dropdown-footer text-center">
                  <router-link to="/minhas-requisicoes" class="text-primary" @click.native="closeNotifications">
                    Ver todas
                  </router-link>
                </div>
              </div>
              </transition>
            </div>
          </div>
        </template>
        

        <!-- se nao for a pagina do login mostra funções extras -->
        <div class="nav-buttons d-flex gap-2 align-items-center" v-if="!isAuthPage">
          <template v-if="isAuthenticated">
            <!-- botões exclusivos para locadores -->
            <template v-if="isLocador">
              <router-link to="/ads" class="btn btn-outline-light">
                <i class="fa-regular fa-rectangle-list me-1"></i>
                Seus anúncios
              </router-link>
              <router-link to="/minhas-locacoes" class="btn btn-outline-light">
                <i class="fa-solid fa-handshake me-1"></i>
                Locações
              </router-link>
              <router-link to="/new-ad" class="btn btn-danger">Anuncie agora!</router-link>
            </template>
            <!-- botões exclusivos para locatários -->
            <template v-else>
              <router-link to="/minhas-requisicoes" class="btn btn-outline-light">
                <i class="fa-solid fa-file-invoice me-1"></i>
                Requisições
              </router-link>
              <router-link to="/minhas-locacoes" class="btn btn-outline-light">
                <i class="fa-solid fa-handshake me-1"></i>
                Locações
              </router-link>
            </template>
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
      <transition name="page" mode="out-in">
        <router-view :key="$route.path"/>  <!--Welcome message do vue-->
      </transition>
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
  data() {
    return {
      showNotifications: false,
      pollingInterval: null
    }
  },
  computed: {
    // página de autenticação (login / register)
    isAuthPage() {
      return this.$route.path === '/login' || this.$route.path === '/register' || this.$route.path === '/forgot-password'
    },

    // estado reativo vindo do vuex
    isAuthenticated() {
      return this.$store.getters['auth/isAuthenticated']
    },

    // usuário atual vindo do vuex
    user() {
      return this.$store.getters['auth/user']
    },

    // verificar se é locador
    isLocador() {
      return this.$store.getters['auth/isLocador']
    },

    // notificações
    requisicoes() {
      return this.$store.getters['notifications/requisicoes']
    },
    mensagens() {
      return this.$store.getters['notifications/mensagens']
    },
    naoLidas() {
      return this.$store.getters['notifications/naoLidas']
    },
    mensagensNaoLidas() {
      return this.$store.getters['notifications/mensagensNaoLidas']
    },
    totalNaoLidas() {
      return this.$store.getters['notifications/totalNaoLidas']
    },
    loadingNotifications() {
      return this.$store.getters['notifications/loading']
    }
  },
  watch: {
    isAuthenticated: {
      immediate: true,
      handler(isAuth) {
        if (isAuth) {
          this.fetchNotifications()
          this.startPolling()
        } else {
          this.$store.dispatch('notifications/clearNotifications')
          this.stopPolling()
        }
      }
    }
  },
  mounted() {
    // fecha dropdown ao clicar fora
    document.addEventListener('click', this.handleClickOutside)
    // verifica sessão no backend se tiver dados salvos no localStorage
    if (this.isAuthenticated) {
      this.$store.dispatch('auth/checkSession')
      this.startPolling()
    }
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside)
    this.stopPolling()
  },
  methods: {
    async handleLogout() {
      await this.$store.dispatch('auth/logout')
      // usar replace e suprimir erros de redirecionamento concorrente
      this.$router.replace('/login').catch(() => {})
    },
    
    toggleNotifications() {
      this.showNotifications = !this.showNotifications
      if (this.showNotifications) {
        this.fetchNotifications()
      }
    },
    
    closeNotifications() {
      this.showNotifications = false
    },
    
    handleClickOutside(event) {
      const btn = this.$refs.notificationBtn
      if (btn && !btn.contains(event.target) && !event.target.closest('.notification-dropdown')) {
        this.showNotifications = false
      }
    },
    
    async fetchNotifications() {
      if (this.isLocador) {
        await this.$store.dispatch('notifications/fetchNotificacoesLocador')
      } else {
        await this.$store.dispatch('notifications/fetchNotificacoesLocatario')
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMs / 3600000)
      const diffDays = Math.floor(diffMs / 86400000)
      
      if (diffMins < 1) return 'agora'
      if (diffMins < 60) return `${diffMins}min`
      if (diffHours < 24) return `${diffHours}h`
      if (diffDays < 7) return `${diffDays}d`
      return date.toLocaleDateString('pt-BR')
    },
    
    statusBadgeClass(status) {
      const classes = {
        'pendente': 'bg-warning text-dark',
        'aceita': 'bg-success',
        'recusada': 'bg-danger',
        'concluida': 'bg-secondary'
      }
      return classes[status] || 'bg-secondary'
    },
    
    getMensagemLink(msg) {
      // Se tem locação, vai pra página da locação com hash pro chat
      if (msg.locacaoId) {
        return `/locacao/${msg.locacaoId}#chat`
      }
      // Senão vai pra requisição com hash pro chat
      return `/requisicao/${msg.requisicaoId}#chat`
    },
    
    startPolling() {
      // busca notificações a cada 10 segundos
      if (this.pollingInterval) return
      this.pollingInterval = setInterval(() => {
        this.fetchNotifications()
      }, 10000)
    },
    
    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval)
        this.pollingInterval = null
      }
    },
    
    getImageUrl(path) {
      if (!path) return null
      if (path.startsWith('http')) return path
      return `http://localhost:8000${path}`
    }
  }
}
</script>

<style lang="scss">
html, body, #wrapper {
  min-height: 100vh;
}

#wrapper {
  display: flex;
  flex-direction: column;
}

section {
  flex: 1 0 auto;
}

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
  font-size: 1.4rem;
  padding: 0.5rem;
  line-height: 1;
}

.btn-icon:hover {
  color: #ffffff;
}

.notifications .btn-icon {
  font-size: 1.3rem;
  padding: 0.25rem;
  position: relative;
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

/* dropdown de notificações */
.notifications .dropdown {
  position: relative;
}

.notification-badge {
  font-size: 0.7rem;
  font-weight: 700;
  color: #fff;
  background-color: #dc3545;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: -4px;
  right: -6px;
  border-radius: 50%;
}

.notification-dropdown {
  position: absolute;
  right: 0;
  top: 100%;
  width: 360px;
  max-height: 480px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  z-index: 1050;
  margin-top: 10px;
  overflow: hidden;
}

.notification-dropdown .dropdown-header {
  padding: 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-weight: 600;
  color: #333;
}

.notification-list {
  max-height: 350px;
  overflow-y: auto;
}

.notification-item {
  padding: 12px 15px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
  text-decoration: none;
  color: inherit;
  display: block;
}

.notification-item:hover {
  background-color: #f8f9fa;
  color: inherit;
}

.notification-item.unread {
  background-color: #f0f7ff;
}

.notification-item.unread:hover {
  background-color: #e3f0ff;
}

.notification-image {
  width: 45px;
  height: 45px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}

.notification-image-placeholder {
  width: 45px;
  height: 45px;
  border-radius: 8px;
  background: linear-gradient(135deg, #17a2b8, #138496);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.notification-title {
  font-weight: 600;
  font-size: 0.85rem;
  color: #333;
}

.notification-text {
  font-size: 0.85rem;
  color: #555;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notification-meta {
  font-size: 0.75rem;
  color: #888;
  margin-top: 2px;
}

.notification-meta .badge {
  font-size: 0.65rem;
  text-transform: capitalize;
}

.unread-dot {
  width: 8px;
  height: 8px;
  background: #007bff;
  border-radius: 50%;
  flex-shrink: 0;
  margin-left: 8px;
}

.dropdown-footer {
  padding: 12px;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

.dropdown-footer a {
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
}

/* ==================== ANIMAÇÕES ==================== */

/* Badge pulsando */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.7);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 0 0 0 8px rgba(220, 53, 69, 0);
  }
}

.notification-badge {
  animation: pulse 2s ease-in-out infinite;
}

/* Dropdown animação */
.dropdown-enter-active {
  animation: dropdownIn 0.25s ease-out;
}

.dropdown-leave-active {
  animation: dropdownOut 0.2s ease-in;
}

@keyframes dropdownIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes dropdownOut {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
}

/* Itens do dropdown entrada escalonada */
.notification-item {
  animation: slideInRight 0.3s ease-out backwards;
}

.notification-item:nth-child(1) { animation-delay: 0.05s; }
.notification-item:nth-child(2) { animation-delay: 0.1s; }
.notification-item:nth-child(3) { animation-delay: 0.15s; }
.notification-item:nth-child(4) { animation-delay: 0.2s; }
.notification-item:nth-child(5) { animation-delay: 0.25s; }

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Page transitions */
.page-enter-active {
  animation: pageEnter 0.35s ease-out;
}

.page-leave-active {
  animation: pageLeave 0.25s ease-in;
}

@keyframes pageEnter {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pageLeave {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-20px);
  }
}

/* Unread dot pulsando */
@keyframes dotPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.3);
  }
}

.unread-dot {
  animation: dotPulse 1.5s ease-in-out infinite;
}
</style>

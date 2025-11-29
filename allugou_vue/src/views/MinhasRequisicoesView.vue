<template>
  <div class="container mt-4">
    <h2 class="mb-4">Minhas Requisições</h2>
    
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Carregando...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else-if="requisicoes.length === 0" class="text-center py-5">
      <i class="fa fa-inbox fa-3x text-muted mb-3 d-block"></i>
      <p class="text-muted">Você ainda não fez nenhuma requisição de locação.</p>
      <router-link to="/" class="btn btn-primary">
        <i class="fa fa-search me-2"></i>Explorar ofertas
      </router-link>
    </div>

    <div v-else class="row g-3">
      <transition-group name="list" appear>
        <div v-for="(req, index) in requisicoes" :key="req.id" class="col-12" :style="{ '--item-index': index }">
          <div class="card requisicao-card" :class="statusClass(req)">
          <div class="card-body">
            <div class="row align-items-center">
              <!-- imagem da oferta -->
              <div class="col-md-2 col-sm-3">
                <img 
                  v-if="req.oferta.imagemPrincipal" 
                  :src="getImageUrl(req.oferta.imagemPrincipal)" 
                  class="img-fluid rounded requisicao-img"
                  alt="imagem oferta"
                >
                <div v-else class="bg-secondary rounded d-flex align-items-center justify-content-center requisicao-img">
                  <i class="fa fa-image fa-2x text-white"></i>
                </div>
              </div>
              
              <!-- info da requisição -->
              <div class="col-md-6 col-sm-9">
                <h5 class="mb-1">{{ req.oferta.titulo }}</h5>
                <p class="text-muted small mb-2">
                  <i class="fa fa-user me-1"></i>
                  Locador: {{ req.locador.nome }}
                </p>
                <p class="text-muted small mb-2">
                  <i class="fa fa-calendar me-1"></i>
                  Início: {{ formatDateLong(req.dataInicioLocacao) }}
                </p>
                <p class="text-muted small mb-0">
                  <i class="fa fa-clock me-1"></i>
                  Solicitado em: {{ formatDateTime(req.dataCriacao) }}
                </p>
              </div>
              
              <!-- status e ações -->
              <div class="col-md-4 text-md-end mt-3 mt-md-0">
                <span class="badge mb-2 d-inline-block" :class="statusBadgeClass(req)">
                  <i :class="statusIcon(req)" class="me-1"></i>
                  {{ statusText(req) }}
                </span>
                
                <div class="d-flex gap-2 justify-content-md-end mt-2">
                  <!-- Sempre mostra link para a requisição -->
                  <router-link 
                    :to="`/requisicao/${req.id}`" 
                    class="btn btn-sm btn-primary"
                  >
                    <i class="fa fa-eye me-1"></i>Ver detalhes
                  </router-link>
                  <!-- Se já tem locação, mostra link adicional para locação -->
                  <router-link 
                    v-if="req.locacaoId"
                    :to="`/locacao/${req.locacaoId}`" 
                    class="btn btn-sm btn-success"
                  >
                    <i class="fa fa-handshake me-1"></i>Ver locação
                  </router-link>
                  <router-link 
                    :to="`/oferta/${req.oferta.id}`" 
                    class="btn btn-sm btn-outline-secondary"
                  >
                    <i class="fa fa-external-link me-1"></i>Ver oferta
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          
          <!-- barra de progresso visual -->
          <div class="card-footer bg-transparent border-top-0 py-2">
            <div class="progress" style="height: 4px;">
              <div 
                class="progress-bar" 
                :class="progressBarClass(req)"
                :style="{ width: progressWidth(req) }"
              ></div>
            </div>
            <div class="d-flex justify-content-between mt-1">
              <small class="text-muted">Enviada</small>
              <small class="text-muted">Aceita</small>
              <small class="text-muted">{{ req.status === 'recusada' ? 'Recusada' : 'Paga' }}</small>
            </div>
          </div>
        </div>
      </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'MinhasRequisicoesView',
  data() {
    return {
      requisicoes: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.loadRequisicoes()
  },
  methods: {
    async loadRequisicoes() {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get('/api/notificacoes/locatario/')
        
        if (response.data.success) {
          this.requisicoes = response.data.requisicoes
        } else {
          this.error = response.data.message || 'erro ao carregar requisições'
        }
      } catch (err) {
        console.error('erro ao carregar requisições:', err)
        this.error = err.response?.data?.message || 'erro ao carregar requisições'
      } finally {
        this.loading = false
      }
    },
    
    getImageUrl(path) {
      if (!path) return null
      if (path.startsWith('http')) return path
      return `http://localhost:8000${path}`
    },
    
    formatDateLong(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
      })
    },
    
    formatDateTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    statusClass(req) {
      // Se já tem locação, mostra como concluída (paga)
      if (req.locacaoId) {
        return 'border-info'
      }
      const classes = {
        'pendente': 'border-warning',
        'aceita': 'border-success',
        'recusada': 'border-danger'
      }
      return classes[req.status] || ''
    },
    
    statusBadgeClass(req) {
      // Se já tem locação, mostra badge diferente
      if (req.locacaoId) {
        return 'bg-info'
      }
      const classes = {
        'pendente': 'bg-warning text-dark',
        'aceita': 'bg-success',
        'recusada': 'bg-danger'
      }
      return classes[req.status] || 'bg-secondary'
    },
    
    statusText(req) {
      // Se já tem locação, mostra status da locação
      if (req.locacaoId) {
        const locacaoTexts = {
          'ativa': 'Pago - Aguardando entrega',
          'em_uso': 'Em uso',
          'devolvida': 'Devolvido',
          'concluida': 'Concluída',
          'cancelada': 'Cancelada'
        }
        return locacaoTexts[req.locacaoStatus] || 'Pago'
      }
      const texts = {
        'pendente': 'Aguardando resposta',
        'aceita': 'Aguardando pagamento',
        'recusada': 'Recusada'
      }
      return texts[req.status] || req.status
    },
    
    statusIcon(req) {
      // Se já tem locação
      if (req.locacaoId) {
        const locacaoIcons = {
          'ativa': 'fa fa-truck',
          'em_uso': 'fa fa-hand-holding',
          'devolvida': 'fa fa-rotate-left',
          'concluida': 'fa fa-check-circle',
          'cancelada': 'fa fa-ban'
        }
        return locacaoIcons[req.locacaoStatus] || 'fa fa-check'
      }
      const icons = {
        'pendente': 'fa fa-clock',
        'aceita': 'fa fa-check',
        'recusada': 'fa fa-times'
      }
      return icons[req.status] || 'fa fa-question'
    },
    
    progressBarClass(req) {
      if (req.locacaoId) {
        return 'bg-info'
      }
      const classes = {
        'pendente': 'bg-warning',
        'aceita': 'bg-success',
        'recusada': 'bg-danger'
      }
      return classes[req.status] || 'bg-secondary'
    },
    
    progressWidth(req) {
      // Se já tem locação, progresso completo
      if (req.locacaoId) {
        return '100%'
      }
      const widths = {
        'pendente': '33%',
        'aceita': '66%',
        'recusada': '100%'
      }
      return widths[req.status] || '0%'
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 900px;
}

.requisicao-card {
  border-left-width: 4px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.requisicao-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.requisicao-img {
  width: 100%;
  height: 100px;
  object-fit: cover;
}

.progress {
  border-radius: 2px;
}

.badge {
  font-size: 0.85rem;
  padding: 0.5em 0.8em;
}

/* ==================== ANIMAÇÕES DE LISTA ==================== */

/* Itens entrando com stagger */
.list-enter-active {
  animation: listIn 0.4s ease-out backwards;
  animation-delay: calc(var(--item-index, 0) * 0.1s);
}

.list-leave-active {
  animation: listOut 0.3s ease-in;
}

.list-move {
  transition: transform 0.4s ease;
}

@keyframes listIn {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes listOut {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(30px);
  }
}

/* Progress bar animada */
.progress-bar {
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Badge pulsando para pendente */
@keyframes badgePulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.badge.bg-warning {
  animation: badgePulse 2s ease-in-out infinite;
}
</style>

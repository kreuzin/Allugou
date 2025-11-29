<template>
  <div class="container mt-4">
    <h2 class="mb-4">
      <i class="fa-solid fa-handshake me-2"></i>
      Minhas Locações
    </h2>
    
    <!-- Tabs para filtrar por status -->
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: filtroStatus === 'todas' }" href="#" @click.prevent="filtroStatus = 'todas'">
          Todas <span class="badge bg-secondary ms-1">{{ locacoes.length }}</span>
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: filtroStatus === 'ativas' }" href="#" @click.prevent="filtroStatus = 'ativas'">
          Em Andamento <span class="badge bg-primary ms-1">{{ locacoesAtivas.length }}</span>
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: filtroStatus === 'concluidas' }" href="#" @click.prevent="filtroStatus = 'concluidas'">
          Concluídas <span class="badge bg-success ms-1">{{ locacoesConcluidas.length }}</span>
        </a>
      </li>
    </ul>
    
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Carregando...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else-if="locacoesFiltradas.length === 0" class="text-center py-5">
      <i class="fa-solid fa-box-open fa-3x text-muted mb-3 d-block"></i>
      <p class="text-muted">
        {{ filtroStatus === 'todas' ? 'Você ainda não tem nenhuma locação.' : 'Nenhuma locação encontrada com este filtro.' }}
      </p>
      <router-link to="/" class="btn btn-primary">
        <i class="fa fa-search me-2"></i>Explorar ofertas
      </router-link>
    </div>

    <div v-else class="row g-3">
      <transition-group name="list" appear>
        <div v-for="(loc, index) in locacoesFiltradas" :key="loc.id" class="col-12" :style="{ '--item-index': index }">
          <div class="card locacao-card" :class="statusBorderClass(loc.status)">
          <div class="card-body">
            <div class="row align-items-center">
              <!-- imagem da oferta -->
              <div class="col-md-2 col-sm-3">
                <img 
                  v-if="loc.oferta.imagemPrincipal" 
                  :src="getImageUrl(loc.oferta.imagemPrincipal)" 
                  class="img-fluid rounded locacao-img"
                  alt="imagem oferta"
                >
                <div v-else class="bg-secondary rounded d-flex align-items-center justify-content-center locacao-img">
                  <i class="fa fa-image fa-2x text-white"></i>
                </div>
              </div>
              
              <!-- info da locação -->
              <div class="col-md-6 col-sm-9">
                <h5 class="mb-1">{{ loc.titulo }}</h5>
                <p v-if="ehLocatario" class="text-muted small mb-2">
                  <i class="fa fa-user me-1"></i>
                  Locador: {{ loc.locador.nome }}
                </p>
                <p v-if="ehLocador" class="text-muted small mb-2">
                  <i class="fa fa-user me-1"></i>
                  Locatário: {{ loc.locatario.nome }}
                </p>
                <p class="text-muted small mb-2">
                  <i class="fa fa-calendar me-1"></i>
                  Período previsto: {{ formatDateShort(loc.dataInicioPrevista) }} 
                  <span v-if="loc.dataFimPrevista">- {{ formatDateShort(loc.dataFimPrevista) }}</span>
                </p>
                <p v-if="loc.dataInicioReal || loc.dataFimReal" class="text-muted small mb-2">
                  <i class="fa fa-calendar-check me-1 text-success"></i>
                  Real: 
                  <span v-if="loc.dataInicioReal">{{ formatDateTime(loc.dataInicioReal) }}</span>
                  <span v-else>--</span>
                  → 
                  <span v-if="loc.dataFimReal">{{ formatDateTime(loc.dataFimReal) }}</span>
                  <span v-else>em uso</span>
                </p>
                <p class="text-muted small mb-0">
                  <i class="fa fa-money-bill me-1"></i>
                  Valor: <strong class="text-success">R$ {{ parseFloat(loc.valorTotal).toFixed(2) }}</strong>
                </p>
              </div>
              
              <!-- status e ações -->
              <div class="col-md-4 text-md-end mt-3 mt-md-0">
                <span class="badge mb-2 d-inline-block" :class="statusBadgeClass(loc.status)">
                  <i :class="statusIcon(loc.status)" class="me-1"></i>
                  {{ statusText(loc.status) }}
                </span>
                
                <div class="d-flex gap-2 justify-content-md-end mt-2">
                  <router-link 
                    :to="`/locacao/${loc.id}`" 
                    class="btn btn-sm btn-primary"
                  >
                    <i class="fa fa-eye me-1"></i>Ver detalhes
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          
          <!-- barra de progresso -->
          <div class="card-footer bg-transparent border-top-0 py-2">
            <div class="progress" style="height: 4px;">
              <div 
                class="progress-bar" 
                :class="progressBarClass(loc.status)"
                :style="{ width: progressWidth(loc.status) }"
              ></div>
            </div>
            <div class="d-flex justify-content-between mt-1">
              <small class="text-muted">Pago</small>
              <small class="text-muted">Recebido</small>
              <small class="text-muted">Devolvido</small>
              <small class="text-muted">Concluído</small>
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
  name: 'MinhasLocacoesView',
  data() {
    return {
      locacoes: [],
      loading: true,
      error: null,
      filtroStatus: 'todas',
      ehLocador: false,
      ehLocatario: false
    }
  },
  computed: {
    locacoesAtivas() {
      return this.locacoes.filter(l => ['ativa', 'em_uso', 'devolvida'].includes(l.status))
    },
    locacoesConcluidas() {
      return this.locacoes.filter(l => l.status === 'concluida')
    },
    locacoesFiltradas() {
      if (this.filtroStatus === 'ativas') return this.locacoesAtivas
      if (this.filtroStatus === 'concluidas') return this.locacoesConcluidas
      return this.locacoes
    }
  },
  mounted() {
    this.loadLocacoes()
  },
  methods: {
    async loadLocacoes() {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get('/api/locacoes/minhas/')
        
        if (response.data.success) {
          this.locacoes = response.data.locacoes
          this.ehLocador = response.data.ehLocador
          this.ehLocatario = response.data.ehLocatario
        } else {
          this.error = response.data.message || 'Erro ao carregar locações'
        }
      } catch (err) {
        console.error('Erro ao carregar locações:', err)
        this.error = err.response?.data?.message || 'Erro ao carregar locações'
      } finally {
        this.loading = false
      }
    },
    
    getImageUrl(path) {
      if (!path) return null
      if (path.startsWith('http')) return path
      return `http://localhost:8000${path}`
    },
    
    formatDateShort(dateString) {
      if (!dateString) return '--'
      return new Date(dateString + 'T00:00:00').toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    },
    
    formatDateTime(dateString) {
      if (!dateString) return '--'
      return new Date(dateString).toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    statusBorderClass(status) {
      const classes = {
        'ativa': 'border-primary',
        'em_uso': 'border-info',
        'devolvida': 'border-warning',
        'concluida': 'border-success',
        'cancelada': 'border-danger'
      }
      return classes[status] || ''
    },
    
    statusBadgeClass(status) {
      const classes = {
        'ativa': 'bg-primary',
        'em_uso': 'bg-info',
        'devolvida': 'bg-warning text-dark',
        'concluida': 'bg-success',
        'cancelada': 'bg-danger'
      }
      return classes[status] || 'bg-secondary'
    },
    
    statusText(status) {
      const texts = {
        'ativa': 'Aguardando entrega',
        'em_uso': 'Em uso',
        'devolvida': 'Devolvida',
        'concluida': 'Concluída',
        'cancelada': 'Cancelada'
      }
      return texts[status] || status
    },
    
    statusIcon(status) {
      const icons = {
        'ativa': 'fa fa-truck',
        'em_uso': 'fa fa-hand-holding',
        'devolvida': 'fa fa-rotate-left',
        'concluida': 'fa fa-check-circle',
        'cancelada': 'fa fa-ban'
      }
      return icons[status] || 'fa fa-question'
    },
    
    progressBarClass(status) {
      const classes = {
        'ativa': 'bg-primary',
        'em_uso': 'bg-info',
        'devolvida': 'bg-warning',
        'concluida': 'bg-success',
        'cancelada': 'bg-danger'
      }
      return classes[status] || 'bg-secondary'
    },
    
    progressWidth(status) {
      const widths = {
        'ativa': '25%',
        'em_uso': '50%',
        'devolvida': '75%',
        'concluida': '100%',
        'cancelada': '100%'
      }
      return widths[status] || '0%'
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 900px;
}

.locacao-card {
  border-left-width: 4px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.locacao-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.locacao-img {
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

.nav-tabs .nav-link {
  color: #6c757d;
}

.nav-tabs .nav-link.active {
  font-weight: 600;
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

/* Badge pulsando para status ativos */
@keyframes badgePulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.badge.bg-primary,
.badge.bg-info {
  animation: badgePulse 2s ease-in-out infinite;
}
</style>

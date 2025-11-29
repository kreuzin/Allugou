<template>
  <div class="container mt-4">
    <!-- tabs para alternar entre anúncios e requisições -->
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <button 
          class="nav-link" 
          :class="{ active: activeTab === 'anuncios' }"
          @click="activeTab = 'anuncios'"
        >
          <i class="fa fa-box me-2"></i>Seus anúncios
          <span v-if="ofertas.length > 0" class="badge bg-secondary ms-2">{{ ofertas.length }}</span>
        </button>
      </li>
      <li class="nav-item">
        <button 
          class="nav-link" 
          :class="{ active: activeTab === 'requisicoes' }"
          @click="activeTab = 'requisicoes'"
        >
          <i class="fa fa-inbox me-2"></i>Requisições recebidas
          <span v-if="requisicoesPendentes > 0" class="badge bg-danger ms-2">{{ requisicoesPendentes }}</span>
        </button>
      </li>
    </ul>

    <!-- tab de anúncios -->
    <div v-show="activeTab === 'anuncios'">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Seus anúncios</h2>
        <router-link to="/new-ad" class="btn btn-primary">
          <i class="fa fa-plus me-2"></i>Criar novo anúncio
        </router-link>
      </div>
      
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Carregando...</span>
        </div>
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-else-if="ofertas.length === 0" class="text-center py-5">
        <i class="fa fa-inbox fa-3x text-muted mb-3"></i>
        <p class="text-muted">Você ainda não tem anúncios cadastrados.</p>
        <router-link to="/new-ad" class="btn btn-primary">
          <i class="fa fa-plus me-2"></i>Criar primeiro anúncio
        </router-link>
      </div>

      <div v-else class="row g-3">
        <div v-for="oferta in ofertas" :key="oferta.id" class="col-md-6 col-lg-4">
          <div class="card h-100">
            <img 
              v-if="oferta.imagem_principal" 
              :src="getImageUrl(oferta.imagem_principal.imagem)" 
              class="card-img-top"
              alt="imagem principal"
              style="height: 200px; object-fit: cover;"
            >
            <div v-else class="card-img-top bg-secondary d-flex align-items-center justify-content-center" style="height: 200px;">
              <i class="fa fa-image fa-3x text-white"></i>
            </div>
            
            <div class="card-body">
              <h5 class="card-title">{{ oferta.titulo }}</h5>
              <p class="card-text text-muted small description-truncate">{{ oferta.descricao }}</p>
              
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <strong class="text-success">R$ {{ formatPrice(oferta.valorDiaria) }}</strong>
                  <small class="text-muted"> / dia</small>
                </div>
                <span :class="['badge', oferta.ofereceEntrega ? 'bg-info' : 'bg-secondary']">
                  <i class="fa fa-truck me-1"></i>{{ oferta.ofereceEntrega ? 'Entrega' : 'Sem entrega' }}
                </span>
              </div>

              <div class="mt-2">
                <small class="text-muted">
                  <i class="fa fa-images me-1"></i>{{ oferta.imagens?.length || 0 }} imagens
                </small>
              </div>
            </div>
            
            <div class="card-footer bg-white border-top-0">
              <div class="d-flex gap-2">
                <router-link 
                  :to="`/oferta/${oferta.id}`" 
                  class="btn btn-sm btn-outline-info flex-fill"
                >
                  <i class="fa fa-eye me-1"></i>Ver
                </router-link>
                <router-link 
                  :to="`/edit-ad/${oferta.id}`" 
                  class="btn btn-sm btn-outline-primary flex-fill"
                >
                  <i class="fa fa-edit me-1"></i>Editar
                </router-link>
                <button 
                  class="btn btn-sm btn-outline-danger" 
                  @click="confirmDelete(oferta)"
                  :disabled="deletingId === oferta.id"
                >
                  <i v-if="deletingId === oferta.id" class="fa fa-spinner fa-spin me-1"></i>
                  <i v-else class="fa fa-trash me-1"></i>
                  {{ deletingId === oferta.id ? '' : 'Excluir' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- tab de requisições -->
    <div v-show="activeTab === 'requisicoes'">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Requisições recebidas</h2>
        <div class="btn-group">
          <button 
            class="btn btn-sm" 
            :class="filtroStatus === 'todas' ? 'btn-primary' : 'btn-outline-primary'"
            @click="filtroStatus = 'todas'"
          >Todas</button>
          <button 
            class="btn btn-sm" 
            :class="filtroStatus === 'pendente' ? 'btn-warning' : 'btn-outline-warning'"
            @click="filtroStatus = 'pendente'"
          >Pendentes</button>
          <button 
            class="btn btn-sm" 
            :class="filtroStatus === 'aceita' ? 'btn-success' : 'btn-outline-success'"
            @click="filtroStatus = 'aceita'"
          >Aceitas</button>
        </div>
      </div>

      <div v-if="loadingRequisicoes" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Carregando...</span>
        </div>
      </div>

      <div v-else-if="errorRequisicoes" class="alert alert-danger">{{ errorRequisicoes }}</div>

      <div v-else-if="requisicoesFiltradas.length === 0" class="text-center py-5">
        <i class="fa fa-inbox fa-3x text-muted mb-3 d-block"></i>
        <p class="text-muted">
          {{ filtroStatus === 'todas' ? 'Você ainda não recebeu nenhuma requisição.' : `Nenhuma requisição ${filtroStatus}.` }}
        </p>
      </div>

      <div v-else class="row g-3">
        <div v-for="req in requisicoesFiltradas" :key="req.id" class="col-12">
          <div class="card requisicao-card" :class="[statusBorderClass(req.status), { 'unread': !req.vistoPeloLocador }]">
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
                  <div class="d-flex align-items-center mb-1">
                    <h5 class="mb-0 me-2">{{ req.oferta.titulo }}</h5>
                    <span v-if="!req.vistoPeloLocador" class="badge bg-primary">Nova</span>
                  </div>
                  <p class="text-muted small mb-2">
                    <i class="fa fa-user me-1"></i>
                    Solicitante: <strong>{{ req.locatario.nome }}</strong>
                  </p>
                  <p class="text-muted small mb-2">
                    <i class="fa fa-calendar me-1"></i>
                    Data desejada: {{ formatDateLong(req.dataInicioLocacao) }}
                  </p>
                  <p class="text-muted small mb-0">
                    <i class="fa fa-clock me-1"></i>
                    Solicitado em: {{ formatDateTime(req.dataCriacao) }}
                  </p>
                </div>
                
                <!-- status e ações -->
                <div class="col-md-4 text-md-end mt-3 mt-md-0">
                  <span class="badge mb-2 d-inline-block" :class="statusBadgeClass(req.status)">
                    <i :class="statusIcon(req.status)" class="me-1"></i>
                    {{ statusText(req.status) }}
                  </span>
                  
                  <div class="d-flex gap-2 justify-content-md-end mt-2">
                    <router-link 
                      :to="`/requisicao/${req.id}`" 
                      class="btn btn-sm btn-primary"
                    >
                      <i class="fa fa-eye me-1"></i>Ver detalhes
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'AdsView',
  data() {
    return {
      ofertas: [],
      requisicoes: [],
      loading: true,
      loadingRequisicoes: true,
      error: null,
      errorRequisicoes: null,
      activeTab: 'anuncios',
      filtroStatus: 'todas',
      deletingId: null
    }
  },
  computed: {
    requisicoesPendentes() {
      return this.requisicoes.filter(r => r.status === 'pendente').length
    },
    requisicoesFiltradas() {
      if (this.filtroStatus === 'todas') {
        return this.requisicoes
      }
      return this.requisicoes.filter(r => r.status === this.filtroStatus)
    }
  },
  mounted() {
    // verificar se usuário é locador
    if (!this.$store.getters['auth/isLocador']) {
      this.$router.push('/')
      return
    }
    
    this.loadOfertas()
    this.loadRequisicoes()
  },
  methods: {
    async loadOfertas() {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get('/api/ofertas/my/')
        
        if (response.data.success) {
          this.ofertas = response.data.ofertas
        } else {
          this.error = response.data.message || 'erro ao carregar anúncios'
        }
      } catch (err) {
        console.error('erro ao carregar ofertas:', err)
        this.error = err.response?.data?.message || 'erro ao carregar anúncios'
      } finally {
        this.loading = false
      }
    },
    
    async loadRequisicoes() {
      this.loadingRequisicoes = true
      this.errorRequisicoes = null
      
      try {
        const response = await api.get('/api/notificacoes/locador/')
        
        if (response.data.success) {
          this.requisicoes = response.data.requisicoes
        } else {
          this.errorRequisicoes = response.data.message || 'erro ao carregar requisições'
        }
      } catch (err) {
        console.error('erro ao carregar requisições:', err)
        this.errorRequisicoes = err.response?.data?.message || 'erro ao carregar requisições'
      } finally {
        this.loadingRequisicoes = false
      }
    },
    
    getImageUrl(imagePath) {
      if (!imagePath) return null
      if (imagePath.startsWith('http')) return imagePath
      return `http://localhost:8000${imagePath}`
    },
    
    formatPrice(value) {
      return parseFloat(value).toFixed(2).replace('.', ',')
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
    
    statusBorderClass(status) {
      const classes = {
        'pendente': 'border-warning',
        'aceita': 'border-success',
        'recusada': 'border-danger',
        'concluida': 'border-secondary'
      }
      return classes[status] || ''
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
    
    statusText(status) {
      const texts = {
        'pendente': 'Pendente',
        'aceita': 'Aceita',
        'recusada': 'Recusada',
        'concluida': 'Concluída'
      }
      return texts[status] || status
    },
    
    statusIcon(status) {
      const icons = {
        'pendente': 'fa fa-clock',
        'aceita': 'fa fa-check',
        'recusada': 'fa fa-times',
        'concluida': 'fa fa-flag-checkered'
      }
      return icons[status] || 'fa fa-question'
    },
    
    async confirmDelete(oferta) {
      const confirmed = await this.$confirm({
        title: 'Excluir anúncio',
        message: `Tem certeza que deseja excluir "${oferta.titulo}"? Esta ação não pode ser desfeita.`,
        type: 'danger',
        confirmText: 'Excluir',
        cancelText: 'Cancelar'
      })
      
      if (!confirmed) return
      
      this.deletingId = oferta.id
      
      try {
        const response = await api.delete(`/api/ofertas/${oferta.id}/delete/`)
        
        if (response.data.success) {
          // remover da lista localmente
          this.ofertas = this.ofertas.filter(o => o.id !== oferta.id)
          this.$toast.success('Anúncio excluído com sucesso!')
        } else {
          this.$toast.error(response.data.message || 'Erro ao excluir anúncio')
        }
      } catch (err) {
        console.error('Erro ao excluir oferta:', err)
        this.$toast.error(err.response?.data?.message || 'Erro ao excluir anúncio')
      } finally {
        this.deletingId = null
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.nav-tabs .nav-link {
  color: #495057;
  border: none;
  border-bottom: 2px solid transparent;
  padding: 0.75rem 1.25rem;
}

.nav-tabs .nav-link:hover {
  border-color: transparent;
  color: #007bff;
}

.nav-tabs .nav-link.active {
  color: #007bff;
  border-color: transparent;
  border-bottom-color: #007bff;
  background-color: transparent;
}

.requisicao-card {
  border-left-width: 4px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.requisicao-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.requisicao-card.unread {
  background-color: #f8f9ff;
}

.requisicao-img {
  width: 100%;
  height: 100px;
  object-fit: cover;
}

.badge {
  font-size: 0.85rem;
  padding: 0.5em 0.8em;
}

.description-truncate {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
  max-height: 2.8em;
}
</style>

<template>
  <div class="locacao-detail-container py-4">
    <div class="container">
      <!-- loading -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Carregando...</span>
        </div>
      </div>

      <!-- erro -->
      <div v-else-if="error" class="alert alert-danger">
        {{ error }}
        <router-link to="/" class="btn btn-outline-danger btn-sm ms-3">Voltar</router-link>
      </div>

      <!-- conteudo -->
      <div v-else-if="locacao" class="row">
        <!-- coluna principal -->
        <div class="col-lg-8">
          <!-- header com status -->
          <div class="card mb-4 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <h4 class="mb-1">{{ locacao.titulo }}</h4>
                  <p class="text-muted mb-0">Locação #{{ locacao.id }}</p>
                </div>
                <span class="badge fs-6" :class="statusBadgeClass">
                  <i :class="statusIcon" class="me-1"></i>
                  {{ statusText }}
                </span>
              </div>
            </div>
          </div>

          <!-- preview da oferta -->
          <div class="card mb-4 shadow-sm">
            <div class="card-body">
              <div class="d-flex align-items-center">
                <img 
                  v-if="imagemPrincipal" 
                  :src="imagemPrincipal" 
                  class="oferta-thumb me-3"
                  alt="imagem oferta"
                >
                <div v-else class="oferta-thumb-placeholder me-3">
                  <i class="fa-solid fa-image"></i>
                </div>
                <div class="flex-grow-1">
                  <h5 class="mb-1">{{ locacao.oferta.titulo }}</h5>
                  <p class="text-muted mb-0 small">
                    <i class="fa-solid fa-location-dot me-1"></i>
                    {{ locacao.oferta.localizacao || 'Localização não informada' }}
                  </p>
                </div>
                <router-link 
                  :to="`/oferta/${locacao.oferta.id}`" 
                  class="btn btn-outline-primary btn-sm"
                >
                  <i class="fa-solid fa-external-link me-1"></i>
                  Ver oferta
                </router-link>
              </div>
            </div>
          </div>

          <!-- detalhes da locação -->
          <div class="card mb-4 shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0"><i class="fa-solid fa-clipboard-list me-2"></i>Detalhes da Locação</h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <!-- datas previstas (planejamento) -->
                <div class="col-12">
                  <h6 class="text-muted mb-2"><i class="fa-regular fa-calendar me-1"></i> Período Planejado (Requisição)</h6>
                </div>
                <div class="col-md-6">
                  <div class="detail-item">
                    <label class="text-muted small">Início Previsto</label>
                    <div class="fw-semibold">{{ formatDateBR(locacao.dataInicioPrevista) }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-item">
                    <label class="text-muted small">Fim Previsto</label>
                    <div class="fw-semibold">{{ locacao.dataFimPrevista ? formatDateBR(locacao.dataFimPrevista) : 'Não informada' }}</div>
                  </div>
                </div>
                
                <!-- datas reais (efetivo) -->
                <div class="col-12 mt-3">
                  <h6 class="text-muted mb-2"><i class="fa-solid fa-calendar-check me-1"></i> Período Real (Efetivo)</h6>
                </div>
                <div class="col-md-6">
                  <div class="detail-item" :class="{ 'detail-item-success': locacao.dataInicioReal }">
                    <label class="text-muted small">Início Real</label>
                    <div class="fw-semibold">
                      <span v-if="locacao.dataInicioReal">
                        <i class="fa-solid fa-check text-success me-1"></i>
                        {{ formatDate(locacao.dataInicioReal) }}
                      </span>
                      <span v-else class="text-muted">
                        <i class="fa-solid fa-hourglass-half me-1"></i>
                        Aguardando recebimento do produto
                      </span>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-item" :class="{ 'detail-item-success': locacao.dataFimReal }">
                    <label class="text-muted small">Fim Real</label>
                    <div class="fw-semibold">
                      <span v-if="locacao.dataFimReal">
                        <i class="fa-solid fa-check text-success me-1"></i>
                        {{ formatDate(locacao.dataFimReal) }}
                      </span>
                      <span v-else class="text-muted">
                        <i class="fa-solid fa-hourglass-half me-1"></i>
                        Aguardando devolução confirmada
                      </span>
                    </div>
                  </div>
                </div>
                
                <div class="col-md-6">
                  <div class="detail-item">
                    <label class="text-muted small">Modalidade</label>
                    <div class="fw-semibold">
                      <span v-if="locacao.retiradaNoLocal">
                        <i class="fa-solid fa-person-walking me-1 text-info"></i>
                        Retirada no local
                      </span>
                      <span v-else>
                        <i class="fa-solid fa-truck me-1 text-success"></i>
                        Entrega
                      </span>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-item">
                    <label class="text-muted small">Data do Pagamento</label>
                    <div class="fw-semibold">{{ formatDate(locacao.dataPagamento) }}</div>
                  </div>
                </div>
                <div class="col-md-6" v-if="!locacao.retiradaNoLocal">
                  <div class="detail-item">
                    <label class="text-muted small">Valor do Frete</label>
                    <div class="fw-semibold">R$ {{ parseFloat(locacao.valorFrete).toFixed(2) }}</div>
                  </div>
                </div>
                <div class="col-12">
                  <hr>
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="fs-5 fw-bold">Valor Total Pago</span>
                    <span class="fs-4 fw-bold text-success">R$ {{ parseFloat(locacao.valorTotal).toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- timeline do fluxo -->
          <div class="card mb-4 shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0"><i class="fa-solid fa-timeline me-2"></i>Histórico</h5>
            </div>
            <div class="card-body">
              <div class="timeline">
                <div class="timeline-item" :class="{ 'completed': true }">
                  <div class="timeline-marker bg-success"></div>
                  <div class="timeline-content">
                    <strong>Pagamento Realizado</strong>
                    <p class="text-muted small mb-0">{{ formatDate(locacao.dataPagamento) }}</p>
                  </div>
                </div>
                
                <div class="timeline-item" :class="{ 'completed': locacao.locatarioConfirmouRecebimento }">
                  <div class="timeline-marker" :class="locacao.locatarioConfirmouRecebimento ? 'bg-success' : 'bg-secondary'"></div>
                  <div class="timeline-content">
                    <strong>Produto Recebido</strong>
                    <small class="d-block text-info" v-if="!locacao.dataInicioReal">
                      (Início real da locação)
                    </small>
                    <p v-if="locacao.dataInicioReal" class="text-success small mb-0">
                      <i class="fa-solid fa-play me-1"></i>
                      Locação iniciada em {{ formatDate(locacao.dataInicioReal) }}
                    </p>
                    <p v-else class="text-muted small mb-0">Aguardando confirmação</p>
                  </div>
                </div>
                
                <div class="timeline-item" :class="{ 'completed': locacao.dataDevolucao }">
                  <div class="timeline-marker" :class="locacao.dataDevolucao ? 'bg-success' : 'bg-secondary'"></div>
                  <div class="timeline-content">
                    <strong>Produto Devolvido</strong>
                    <p v-if="locacao.dataDevolucao" class="text-muted small mb-0">
                      {{ formatDate(locacao.dataDevolucao) }}
                    </p>
                    <p v-else class="text-muted small mb-0">Aguardando devolução</p>
                  </div>
                </div>
                
                <div class="timeline-item" :class="{ 'completed': locacao.status === 'concluida' }">
                  <div class="timeline-marker" :class="locacao.status === 'concluida' ? 'bg-success' : 'bg-secondary'"></div>
                  <div class="timeline-content">
                    <strong>Locação Concluída</strong>
                    <small class="d-block text-info" v-if="!locacao.dataFimReal">
                      (Fim real da locação)
                    </small>
                    <p v-if="locacao.dataFimReal" class="text-success small mb-0">
                      <i class="fa-solid fa-flag-checkered me-1"></i>
                      Locação finalizada em {{ formatDate(locacao.dataFimReal) }}
                    </p>
                    <p v-else class="text-muted small mb-0">Em andamento</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- chat -->
          <div class="card shadow-sm chat-section">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0"><i class="fa-solid fa-comments me-2"></i>Conversa</h5>
              <small class="text-muted">{{ mensagens.length }} mensagens</small>
            </div>
            <div class="card-body p-0">
              <div class="messages-container" ref="messagesContainer">
                <div v-if="mensagens.length === 0" class="text-center py-5 text-muted">
                  <i class="fa-regular fa-comment-dots fa-3x mb-3"></i>
                  <p>Nenhuma mensagem ainda.</p>
                </div>
                
                <transition-group name="message" tag="div">
                  <div 
                    v-for="msg in mensagens" 
                    :key="msg.id"
                    class="message"
                    :class="{ 
                      'message-own': isOwnMessage(msg.remetente),
                      'message-other': !isOwnMessage(msg.remetente)
                    }"
                  >
                    <div class="message-bubble">
                      <div class="message-sender">
                        {{ msg.remetente === 'locador' ? locacao.locador.nome : locacao.locatario.nome }}
                      </div>
                      <div class="message-text">{{ msg.texto }}</div>
                      <div class="message-time">{{ formatTime(msg.enviadoEm) }}</div>
                    </div>
                  </div>
                </transition-group>
              </div>

              <!-- input mensagem -->
              <div class="message-input-container">
                <form @submit.prevent="enviarMensagem" class="d-flex gap-2">
                  <input 
                    type="text" 
                    v-model="novaMensagem"
                    class="form-control"
                    placeholder="Digite sua mensagem..."
                    :disabled="enviandoMensagem"
                  >
                  <button 
                    type="submit" 
                    class="btn btn-primary"
                    :disabled="enviandoMensagem || !novaMensagem.trim()"
                  >
                    <i class="fa-solid fa-paper-plane"></i>
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>

        <!-- coluna direita - ações e contato -->
        <div class="col-lg-4">
          <!-- card de ações baseado no status -->
          <div class="card mb-4 shadow-sm">
            <div class="card-body text-center py-4">
              <!-- ativa - locatário pode confirmar recebimento -->
              <div v-if="locacao.status === 'ativa'" class="text-primary">
                <i class="fa-solid fa-box fa-3x mb-2"></i>
                <h5>Aguardando Entrega</h5>
                <p class="text-muted small mb-3">
                  <span v-if="ehLocatario">Confirme quando receber o produto.</span>
                  <span v-else>Entregue o produto ao locatário.</span>
                </p>
                <button 
                  v-if="ehLocatario"
                  @click="confirmarRecebimento" 
                  class="btn btn-success btn-lg w-100"
                  :disabled="processando"
                >
                  <i class="fa-solid fa-box-open me-2"></i>
                  Confirmar Recebimento
                </button>
              </div>
              
              <!-- em uso - locatário pode devolver -->
              <div v-else-if="locacao.status === 'em_uso'" class="text-info">
                <i class="fa-solid fa-hand-holding-hand fa-3x mb-2"></i>
                <h5>Produto em Uso</h5>
                <p class="text-muted small mb-3">
                  <span v-if="ehLocatario">Ao devolver, envie uma foto do produto.</span>
                  <span v-else>Aguarde a devolução do produto.</span>
                </p>
                <div v-if="ehLocatario">
                  <input 
                    type="file" 
                    ref="fotoDevolucaoInput"
                    @change="handleFotoSelecionada"
                    accept="image/*"
                    class="d-none"
                  >
                  <button 
                    @click="$refs.fotoDevolucaoInput.click()" 
                    class="btn btn-warning btn-lg w-100"
                    :disabled="processando"
                  >
                    <i class="fa-solid fa-camera me-2"></i>
                    Enviar Foto de Devolução
                  </button>
                  <div v-if="fotoSelecionada" class="mt-3">
                    <img :src="fotoPreview" class="img-thumbnail mb-2" style="max-height: 150px;">
                    <button 
                      @click="enviarFotoDevolucao" 
                      class="btn btn-success w-100"
                      :disabled="processando"
                    >
                      <i class="fa-solid fa-paper-plane me-2"></i>
                      Confirmar Devolução
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- devolvida - locador pode confirmar -->
              <div v-else-if="locacao.status === 'devolvida'" class="text-warning">
                <i class="fa-solid fa-rotate-left fa-3x mb-2"></i>
                <h5>Produto Devolvido</h5>
                <p class="text-muted small mb-3">
                  <span v-if="ehLocador">Confirme o recebimento do produto.</span>
                  <span v-else>Aguardando confirmação do locador.</span>
                </p>
                <div v-if="locacao.fotoDevolucao" class="mb-3">
                  <small class="text-muted d-block mb-2">Foto da devolução:</small>
                  <img :src="getImageUrl(locacao.fotoDevolucao)" class="img-thumbnail" style="max-height: 200px;">
                </div>
                <button 
                  v-if="ehLocador"
                  @click="confirmarDevolucao" 
                  class="btn btn-success btn-lg w-100"
                  :disabled="processando"
                >
                  <i class="fa-solid fa-check-double me-2"></i>
                  Confirmar Recebimento
                </button>
              </div>
              
              <!-- concluída -->
              <div v-else-if="locacao.status === 'concluida'" class="text-secondary">
                <i class="fa-solid fa-flag-checkered fa-3x mb-2"></i>
                <h5>Locação Concluída!</h5>
                <p class="text-muted small mb-0">Esta locação foi finalizada com sucesso.</p>
                <div v-if="locacao.fotoDevolucao" class="mt-3">
                  <small class="text-muted d-block mb-2">Foto da devolução:</small>
                  <img :src="getImageUrl(locacao.fotoDevolucao)" class="img-thumbnail" style="max-height: 150px;">
                </div>
              </div>
              
              <!-- cancelada -->
              <div v-else-if="locacao.status === 'cancelada'" class="text-danger">
                <i class="fa-solid fa-ban fa-3x mb-2"></i>
                <h5>Locação Cancelada</h5>
                <p class="text-muted small mb-0">Esta locação foi cancelada.</p>
              </div>
            </div>
          </div>

          <!-- card de contato -->
          <div class="card mb-4 shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0">
                <i class="fa-solid fa-user me-2"></i>
                {{ ehLocador ? 'Locatário' : 'Locador' }}
              </h5>
            </div>
            <div class="card-body">
              <div class="d-flex align-items-center mb-3">
                <div class="contact-avatar me-3">
                  <i class="fa-solid fa-user"></i>
                </div>
                <div>
                  <h6 class="mb-0">{{ contactName }}</h6>
                  <small class="text-muted">{{ ehLocador ? 'Locatário' : 'Dono do item' }}</small>
                </div>
              </div>
              
              <div class="contact-details">
                <div class="contact-item" v-if="contactEmail">
                  <i class="fa-solid fa-envelope text-muted me-2"></i>
                  <span>{{ contactEmail }}</span>
                </div>
                <div class="contact-item" v-if="contactPhone">
                  <i class="fa-solid fa-phone text-muted me-2"></i>
                  <span>{{ formatPhone(contactPhone) }}</span>
                </div>
                <div class="contact-item" v-if="ehLocador && locacao.locatario.endereco">
                  <i class="fa-solid fa-location-dot text-muted me-2"></i>
                  <span class="small">
                    {{ locacao.locatario.endereco.bairro }}, 
                    {{ locacao.locatario.endereco.cidade }} - 
                    {{ locacao.locatario.endereco.estado }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- botão voltar -->
          <router-link to="/minhas-locacoes" class="btn btn-outline-secondary w-100 mb-2">
            <i class="fa-solid fa-arrow-left me-2"></i>Voltar para Locações
          </router-link>
          <router-link to="/" class="btn btn-outline-secondary w-100">
            <i class="fa-solid fa-home me-2"></i>Ir para Home
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'LocacaoDetailView',
  data() {
    return {
      locacao: null,
      ehLocador: false,
      ehLocatario: false,
      loading: true,
      initialized: false,  // controla se já carregou pela primeira vez
      error: null,
      novaMensagem: '',
      enviandoMensagem: false,
      processando: false,
      fotoSelecionada: null,
      fotoPreview: null,
      pollingInterval: null
    }
  },
  computed: {
    mensagens() {
      return this.locacao?.mensagens || []
    },
    imagemPrincipal() {
      if (!this.locacao?.oferta?.imagens) return null
      const principal = this.locacao.oferta.imagens.find(img => img.ehPrincipal)
      const url = principal?.url || this.locacao.oferta.imagens[0]?.url || null
      return this.getImageUrl(url)
    },
    statusBadgeClass() {
      const classes = {
        'ativa': 'bg-primary',
        'em_uso': 'bg-info',
        'devolvida': 'bg-warning text-dark',
        'concluida': 'bg-success',
        'cancelada': 'bg-danger'
      }
      return classes[this.locacao?.status] || 'bg-secondary'
    },
    statusText() {
      const texts = {
        'ativa': 'Ativa',
        'em_uso': 'Em Uso',
        'devolvida': 'Devolvida',
        'concluida': 'Concluída',
        'cancelada': 'Cancelada'
      }
      return texts[this.locacao?.status] || this.locacao?.status
    },
    statusIcon() {
      const icons = {
        'ativa': 'fa-solid fa-play',
        'em_uso': 'fa-solid fa-hand-holding',
        'devolvida': 'fa-solid fa-rotate-left',
        'concluida': 'fa-solid fa-check',
        'cancelada': 'fa-solid fa-ban'
      }
      return icons[this.locacao?.status] || 'fa-solid fa-question'
    },
    contactName() {
      if (this.ehLocador) {
        return this.locacao?.locatario?.nome
      }
      return this.locacao?.locador?.nome
    },
    contactPhone() {
      if (this.ehLocador) {
        return this.locacao?.locatario?.tel
      }
      return this.locacao?.locador?.tel
    },
    contactEmail() {
      if (this.ehLocador) {
        return this.locacao?.locatario?.email
      }
      return this.locacao?.locador?.email
    }
  },
  async created() {
    await this.fetchLocacao()
    this.startPolling()
    
    // se URL tem #chat, faz scroll pro chat. daora pq diminui a carga cognitiva (design thinking ok? respeita o moço (se pa q na vdd é engenharia semiotica, psicologia cognitiva ou algo assim))
    if (this.$route.hash === '#chat') {
      this.$nextTick(() => {
        this.scrollToChat()
      })
    }
  },
  beforeDestroy() {
    this.stopPolling()
  },
  methods: {
    scrollToChat() {
      const chatSection = document.querySelector('.chat-section')
      if (chatSection) {
        chatSection.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    },
    
    async fetchLocacao() {
      // so mostra loading no primeiro carregamento
      if (!this.initialized) {
        this.loading = true
      }
      this.error = null
      
      try {
        const response = await api.get(`/api/locacoes/${this.$route.params.id}/`)
        
        if (response.data.success) {
          this.locacao = response.data.locacao
          this.ehLocador = response.data.ehLocador
          this.ehLocatario = response.data.ehLocatario
          this.initialized = true
          
          this.$nextTick(() => {
            this.scrollToBottom()
          })
        } else {
          this.error = response.data.message || 'Erro ao carregar locação'
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Erro ao carregar locação'
      } finally {
        this.loading = false
      }
    },
    
    async enviarMensagem() {
      if (!this.novaMensagem.trim()) return
      
      this.enviandoMensagem = true
      
      try {
        const response = await api.post(`/api/locacoes/${this.locacao.id}/mensagem/`, {
          texto: this.novaMensagem.trim()
        })
        
        if (response.data.success) {
          this.locacao.mensagens.push(response.data.mensagem)
          this.novaMensagem = ''
          this.$nextTick(() => {
            this.scrollToBottom()
          })
        }
      } catch (err) {
        console.error('Erro ao enviar mensagem:', err)
        this.$toast.error('Erro ao enviar mensagem')
      } finally {
        this.enviandoMensagem = false
      }
    },
    
    async confirmarRecebimento() {
      const confirmed = await this.$confirm({
        title: 'Confirmar recebimento',
        message: 'Você confirma que recebeu o produto?',
        type: 'question',
        confirmText: 'Confirmar',
        cancelText: 'Cancelar'
      })
      
      if (!confirmed) return
      
      this.processando = true
      
      try {
        const response = await api.post(`/api/locacoes/${this.locacao.id}/confirmar-recebimento/`)
        
        if (response.data.success) {
          this.locacao.status = 'em_uso'
          this.locacao.locatarioConfirmouRecebimento = true
          this.locacao.dataConfirmacaoRecebimento = new Date().toISOString()
          this.$toast.success('Recebimento confirmado!')
        } else {
          this.$toast.error(response.data.message || 'Erro ao confirmar recebimento')
        }
      } catch (err) {
        this.$toast.error(err.response?.data?.message || 'Erro ao confirmar recebimento')
      } finally {
        this.processando = false
      }
    },
    
    handleFotoSelecionada(event) {
      const file = event.target.files[0]
      if (file) {
        this.fotoSelecionada = file
        this.fotoPreview = URL.createObjectURL(file)
      }
    },
    
    async enviarFotoDevolucao() {
      if (!this.fotoSelecionada) {
        this.$toast.warning('Selecione uma foto primeiro')
        return
      }
      
      const confirmed = await this.$confirm({
        title: 'Confirmar devolução',
        message: 'Você confirma a devolução do produto?',
        type: 'question',
        confirmText: 'Confirmar',
        cancelText: 'Cancelar'
      })
      
      if (!confirmed) return
      
      this.processando = true
      
      try {
        const formData = new FormData()
        formData.append('foto', this.fotoSelecionada)
        
        const response = await api.post(
          `/api/locacoes/${this.locacao.id}/foto-devolucao/`,
          formData,
          { headers: { 'Content-Type': 'multipart/form-data' } }
        )
        
        if (response.data.success) {
          this.locacao.status = 'devolvida'
          this.locacao.fotoDevolucao = response.data.foto_url
          this.locacao.dataDevolucao = new Date().toISOString()
          this.fotoSelecionada = null
          this.fotoPreview = null
          this.$toast.success('Foto de devolução enviada!')
        } else {
          this.$toast.error(response.data.message || 'Erro ao enviar foto')
        }
      } catch (err) {
        this.$toast.error(err.response?.data?.message || 'Erro ao enviar foto')
      } finally {
        this.processando = false
      }
    },
    
    async confirmarDevolucao() {
      const confirmed = await this.$confirm({
        title: 'Confirmar recebimento',
        message: 'Você confirma que recebeu o produto de volta?',
        type: 'success',
        confirmText: 'Confirmar',
        cancelText: 'Cancelar'
      })
      
      if (!confirmed) return
      
      this.processando = true
      
      try {
        const response = await api.post(`/api/locacoes/${this.locacao.id}/confirmar-devolucao/`)
        
        if (response.data.success) {
          this.locacao.status = 'concluida'
          this.locacao.locadorConfirmouDevolucao = true
          this.locacao.dataConfirmacaoDevolucao = new Date().toISOString()
          this.locacao.dataConclusao = new Date().toISOString()
          this.$toast.success('Locação concluída com sucesso!', 'Parabéns!')
        } else {
          this.$toast.error(response.data.message || 'Erro ao confirmar devolução')
        }
      } catch (err) {
        this.$toast.error(err.response?.data?.message || 'Erro ao confirmar devolução')
      } finally {
        this.processando = false
      }
    },
    
    isOwnMessage(remetente) {
      if (this.ehLocador && remetente === 'locador') return true
      if (this.ehLocatario && remetente === 'locatario') return true
      return false
    },
    
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    formatDateBR(dateString) {
      return new Date(dateString + 'T00:00:00').toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
      })
    },
    
    formatTime(dateString) {
      return new Date(dateString).toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    formatPhone(phone) {
      if (!phone) return ''
      const cleaned = phone.replace(/\D/g, '')
      if (cleaned.length === 11) {
        return `(${cleaned.slice(0,2)}) ${cleaned.slice(2,7)}-${cleaned.slice(7)}`
      }
      return phone
    },
    
    getImageUrl(path) {
      if (!path) return null
      if (path.startsWith('http')) return path
      return `http://localhost:8000${path}`
    },
    
    startPolling() {
      // atualiza a cada 10 segundos (silenciosamente)
      this.pollingInterval = setInterval(() => {
        this.fetchLocacao()
      }, 10000)
    },
    
    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval)
        this.pollingInterval = null
      }
    }
  }
}
</script>

<style scoped>
.locacao-detail-container {
  background: #f5f7fa;
  min-height: 100vh;
}

.oferta-thumb {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  object-fit: cover;
}

.oferta-thumb-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #adb5bd;
  font-size: 1.5rem;
}

.detail-item {
  padding: 10px;
  background: #f8f9fa;
  border-radius: 8px;
}

.detail-item label {
  display: block;
  margin-bottom: 4px;
}

.detail-item-success {
  background: #d1e7dd;
  border: 1px solid #badbcc;
}

/* timeline */
.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e9ecef;
}

.timeline-item {
  position: relative;
  padding-bottom: 20px;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-marker {
  position: absolute;
  left: -26px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
}

.timeline-item.completed .timeline-marker {
  box-shadow: 0 0 0 3px rgba(25, 135, 84, 0.2);
}

.timeline-content {
  padding-left: 10px;
}

/* Mensagens */
.messages-container {
  height: 300px;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
}

.message {
  margin-bottom: 16px;
  display: flex;
}

.message-own {
  justify-content: flex-end;
}

.message-other {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 16px;
}

.message-own .message-bubble {
  background: #007bff;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-other .message-bubble {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.message-sender {
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 4px;
  opacity: 0.8;
}

.message-text {
  word-break: break-word;
}

.message-time {
  font-size: 0.7rem;
  opacity: 0.7;
  text-align: right;
  margin-top: 4px;
}

.message-input-container {
  padding: 15px;
  background: white;
  border-top: 1px solid #e9ecef;
}

/* Contato */
.contact-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00695c, #004d40);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}

.contact-details {
  border-top: 1px solid #e9ecef;
  padding-top: 15px;
}

.contact-item {
  padding: 8px 0;
  display: flex;
  align-items: center;
}

.contact-item i {
  width: 20px;
}

/* ==================== animações do chat ==================== */

/* mensagens entrando */
.message-enter-active {
  animation: messageIn 0.3s ease-out;
}

.message-leave-active {
  animation: messageOut 0.2s ease-in;
}

@keyframes messageIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes messageOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-10px);
  }
}

/* mensagem própria entra da direita */
.message-own.message-enter-active {
  animation: messageOwnIn 0.3s ease-out;
}

@keyframes messageOwnIn {
  from {
    opacity: 0;
    transform: translateX(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

/* mensagem do outro entra da esquerda */
.message-other.message-enter-active {
  animation: messageOtherIn 0.3s ease-out;
}

@keyframes messageOtherIn {
  from {
    opacity: 0;
    transform: translateX(-30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

/* botão enviar com feedback */
.message-input-container .btn-primary {
  transition: all 0.2s ease;
}

.message-input-container .btn-primary:not(:disabled):hover {
  transform: scale(1.05);
}

.message-input-container .btn-primary:not(:disabled):active {
  transform: scale(0.95);
}

/* timeline animação */
.timeline-item {
  animation: timelineIn 0.4s ease-out backwards;
}

.timeline-item:nth-child(1) { animation-delay: 0.1s; }
.timeline-item:nth-child(2) { animation-delay: 0.2s; }
.timeline-item:nth-child(3) { animation-delay: 0.3s; }
.timeline-item:nth-child(4) { animation-delay: 0.4s; }

@keyframes timelineIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* cards com hover suave */
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
}

/* badge de status com pulso quando em andamento */
@keyframes statusPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.badge.bg-primary,
.badge.bg-info {
  animation: statusPulse 2s ease-in-out infinite;
}
</style>

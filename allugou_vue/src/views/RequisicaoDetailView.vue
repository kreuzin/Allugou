<template>
  <div class="requisicao-detail-container">
    <div class="container py-4">
      <!-- carregando -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Carregando...</span>
        </div>
      </div>

      <!-- erro -->
      <div v-else-if="error" class="alert alert-danger text-center">
        {{ error }}
        <br>
        <router-link to="/" class="btn btn-outline-primary mt-3">Voltar para Home</router-link>
      </div>

      <!-- conteudo principal -->
      <div v-else-if="requisicao" class="row">
        <!-- coluna esquerda - info da oferta -->
        <div class="col-lg-8">
          <!-- card do cabecalho -->
          <div class="card mb-4 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h4 class="mb-1">Requisição #{{ requisicao.id }}</h4>
                  <span class="badge" :class="statusBadgeClass">{{ statusText }}</span>
                </div>
                <small class="text-muted">{{ formatDate(requisicao.dataCriacao) }}</small>
              </div>

              <!-- preview da oferta -->
              <div class="oferta-preview p-3 bg-light rounded">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <img 
                      v-if="imagemPrincipal" 
                      :src="imagemPrincipal" 
                      class="oferta-thumb"
                      alt="Oferta"
                    >
                    <div v-else class="oferta-thumb-placeholder">
                      <i class="fa-solid fa-image"></i>
                    </div>
                  </div>
                  <div class="col">
                    <h5 class="mb-1">{{ requisicao.oferta.titulo }}</h5>
                    <p class="text-muted mb-1 small">{{ requisicao.oferta.descricao }}</p>
                    <div class="text-muted small">
                      <i class="fa-solid fa-location-dot me-1"></i>
                      {{ requisicao.oferta.localizacao }}
                    </div>
                  </div>
                  <div class="col-auto text-end">
                    <div class="text-primary fw-bold fs-5">
                      R$ {{ parseFloat(requisicao.oferta.valorDiaria).toFixed(2) }}
                      <small class="text-muted fw-normal">/dia</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- card de detalhes da requisicao -->
          <div class="card mb-4 shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0"><i class="fa-solid fa-clipboard-list me-2"></i>Detalhes da Requisição</h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <div class="detail-item">
                    <label class="text-muted small">Data de Início</label>
                    <div class="fw-semibold">{{ formatDateBR(requisicao.dataInicioLocacao) }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-item">
                    <label class="text-muted small">Data de Fim</label>
                    <div class="fw-semibold">{{ requisicao.dataFimLocacao ? formatDateBR(requisicao.dataFimLocacao) : 'Não informada' }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="detail-item">
                    <label class="text-muted small">Modalidade</label>
                    <div class="fw-semibold">
                      <span v-if="requisicao.retiradaNoLocal">
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
                    <label class="text-muted small">Valor da Diária</label>
                    <div class="fw-semibold">R$ {{ parseFloat(requisicao.oferta.valorDiaria).toFixed(2) }}</div>
                  </div>
                </div>
                <div class="col-md-6" v-if="!requisicao.retiradaNoLocal">
                  <div class="detail-item">
                    <label class="text-muted small">Valor do Frete</label>
                    <div class="fw-semibold">R$ {{ parseFloat(requisicao.valorFrete).toFixed(2) }}</div>
                  </div>
                </div>
                <div class="col-12">
                  <hr>
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="fs-5 fw-bold">Valor Total</span>
                    <span class="fs-4 fw-bold text-success">R$ {{ parseFloat(requisicao.valorTotal).toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- secao do chat -->
          <div class="card shadow-sm chat-section">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0"><i class="fa-solid fa-comments me-2"></i>Conversa</h5>
              <small class="text-muted">{{ mensagens.length }} mensagens</small>
            </div>
            <div class="card-body p-0">
              <!-- lista de mensagens -->
              <div class="messages-container" ref="messagesContainer">
                <div v-if="mensagens.length === 0" class="text-center py-5 text-muted">
                  <i class="fa-regular fa-comment-dots fa-3x mb-3"></i>
                  <p>Nenhuma mensagem ainda.<br>Inicie a conversa!</p>
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
                        {{ msg.remetente === 'locador' ? requisicao.oferta.locador.nome : requisicao.locatario.nome }}
                      </div>
                      <div class="message-text">{{ msg.texto }}</div>
                      <div class="message-time">{{ formatTime(msg.enviadoEm) }}</div>
                    </div>
                  </div>
                </transition-group>
              </div>

              <!-- campo de mensagem -->
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
                    :disabled="!novaMensagem.trim() || enviandoMensagem"
                  >
                    <i v-if="enviandoMensagem" class="fa-solid fa-spinner fa-spin"></i>
                    <i v-else class="fa-solid fa-paper-plane"></i>
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>

        <!-- coluna direita - acoes e contato -->
        <div class="col-lg-4">
          <!-- acoes do locador (se for locador e pendente) -->
          <div v-if="ehLocador && requisicao.status === 'pendente'" class="card mb-4 shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0"><i class="fa-solid fa-gavel me-2"></i>Ações</h5>
            </div>
            <div class="card-body">
              <p class="text-muted small mb-3">
                O locatário <strong>{{ requisicao.locatario.nome }}</strong> quer alugar seu item.
              </p>
              <div class="d-grid gap-2">
                <button 
                  @click="atualizarStatus('aceita')" 
                  class="btn btn-success"
                  :disabled="atualizandoStatus"
                >
                  <i class="fa-solid fa-check me-2"></i>Aceitar Requisição
                </button>
                <button 
                  @click="atualizarStatus('recusada')" 
                  class="btn btn-outline-danger"
                  :disabled="atualizandoStatus"
                >
                  <i class="fa-solid fa-times me-2"></i>Recusar
                </button>
              </div>
            </div>
          </div>

          <!-- card de status e ações dinâmicas -->
          <div v-if="requisicao.status !== 'pendente'" class="card mb-4 shadow-sm">
            <div class="card-body text-center py-4">
              <!-- aceita - locatario pode pagar -->
              <div v-if="requisicao.status === 'aceita' && !requisicao.locacaoId" class="text-success">
                <i class="fa-solid fa-circle-check fa-3x mb-2"></i>
                <h5>Requisição Aceita!</h5>
                <p class="text-muted small mb-3">
                  <span v-if="ehLocatario">Efetue o pagamento para iniciar a locação.</span>
                  <span v-else>Aguardando pagamento do locatário.</span>
                </p>
                <button 
                  v-if="ehLocatario"
                  @click="realizarPagamento" 
                  class="btn btn-primary btn-lg w-100"
                  :disabled="processando"
                >
                  <i class="fa-solid fa-credit-card me-2"></i>
                  Realizar Pagamento
                </button>
              </div>
              
              <!-- aceita com locação criada - redirecionar -->
              <div v-else-if="requisicao.status === 'aceita' && requisicao.locacaoId" class="text-primary">
                <i class="fa-solid fa-handshake fa-3x mb-2"></i>
                <h5>Locação em Andamento!</h5>
                <p class="text-muted small mb-3">
                  O pagamento foi realizado e a locação está ativa.
                </p>
                <router-link 
                  :to="`/locacao/${requisicao.locacaoId}`" 
                  class="btn btn-primary btn-lg w-100"
                >
                  <i class="fa-solid fa-arrow-right me-2"></i>
                  Ver Locação
                </router-link>
              </div>
              
              <!-- recusada -->
              <div v-else-if="requisicao.status === 'recusada'" class="text-danger">
                <i class="fa-solid fa-circle-xmark fa-3x mb-2"></i>
                <h5>Requisição Recusada</h5>
                <p class="text-muted small mb-0">Infelizmente esta requisição foi recusada.</p>
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
                  <small class="text-muted">{{ ehLocador ? 'Interessado no aluguel' : 'Dono do item' }}</small>
                </div>
              </div>
              
              <div v-if="statusPermiteContato || ehLocador" class="contact-details">
                <div class="contact-item">
                  <i class="fa-solid fa-envelope text-muted me-2"></i>
                  <span>{{ contactEmail }}</span>
                </div>
                <div class="contact-item" v-if="contactPhone">
                  <i class="fa-solid fa-phone text-muted me-2"></i>
                  <span>{{ formatPhone(contactPhone) }}</span>
                </div>
                <div class="contact-item" v-if="ehLocador && requisicao.locatario.endereco">
                  <i class="fa-solid fa-location-dot text-muted me-2"></i>
                  <span class="small">
                    {{ requisicao.locatario.endereco.bairro }}, 
                    {{ requisicao.locatario.endereco.cidade }} - 
                    {{ requisicao.locatario.endereco.estado }}
                  </span>
                </div>
              </div>
              
              <div v-else class="text-muted small text-center py-2">
                <i class="fa-solid fa-lock me-1"></i>
                Contato disponível após aceite
              </div>
            </div>
          </div>

          <!-- botao voltar -->
          <router-link to="/" class="btn btn-outline-secondary w-100">
            <i class="fa-solid fa-arrow-left me-2"></i>Voltar para Home
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'RequisicaoDetailView',
  data() {
    return {
      requisicao: null,
      ehLocador: false,
      ehLocatario: false,
      loading: true,
      error: null,
      novaMensagem: '',
      enviandoMensagem: false,
      atualizandoStatus: false,
      chatPollingInterval: null,
      processando: false
    }
  },
  computed: {
    mensagens() {
      return this.requisicao?.mensagens || []
    },
    imagemPrincipal() {
      if (!this.requisicao?.oferta?.imagens) return null
      const principal = this.requisicao.oferta.imagens.find(img => img.ehPrincipal)
      const url = principal?.url || this.requisicao.oferta.imagens[0]?.url || null
      return this.getImageUrl(url)
    },
    statusBadgeClass() {
      const classes = {
        'pendente': 'bg-warning text-dark',
        'aceita': 'bg-success',
        'recusada': 'bg-danger'
      }
      return classes[this.requisicao?.status] || 'bg-secondary'
    },
    statusText() {
      const texts = {
        'pendente': 'Aguardando resposta',
        'aceita': this.requisicao?.locacaoId ? 'Locação Iniciada' : 'Aceita - Aguardando pagamento',
        'recusada': 'Recusada'
      }
      return texts[this.requisicao?.status] || this.requisicao?.status
    },
    statusPermiteContato() {
      // mostra contato quando aceita
      return this.requisicao?.status === 'aceita'
    },
    contactName() {
      if (this.ehLocador) {
        return this.requisicao?.locatario?.nome
      }
      return this.requisicao?.oferta?.locador?.nome
    },
    contactEmail() {
      if (this.ehLocador) {
        return this.requisicao?.locatario?.email
      }
      // email do locador nao ta disponivel ainda
      return null
    },
    contactPhone() {
      if (this.ehLocador) {
        return this.requisicao?.locatario?.tel
      }
      return this.requisicao?.oferta?.locador?.tel
    }
  },
  async created() {
    await this.fetchRequisicao()
    this.startChatPolling()
    
    // Se URL tem #chat, faz scroll pro chat
    if (this.$route.hash === '#chat') {
      this.$nextTick(() => {
        this.scrollToChat()
      })
    }
  },
  beforeDestroy() {
    this.stopChatPolling()
  },
  methods: {
    scrollToChat() {
      const chatSection = document.querySelector('.chat-section')
      if (chatSection) {
        chatSection.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    },
    
    async fetchRequisicao() {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get(`/api/requisicoes/${this.$route.params.id}/`)
        
        if (response.data.success) {
          this.requisicao = response.data.requisicao
          this.ehLocador = response.data.ehLocador
          this.ehLocatario = response.data.ehLocatario
          
          // rola pra ultima mensagem
          this.$nextTick(() => {
            this.scrollToBottom()
          })
        } else {
          this.error = response.data.message || 'Erro ao carregar requisição'
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Erro ao carregar requisição'
      } finally {
        this.loading = false
      }
    },
    
    async enviarMensagem() {
      if (!this.novaMensagem.trim()) return
      
      this.enviandoMensagem = true
      
      try {
        const response = await api.post(`/api/requisicoes/${this.requisicao.id}/mensagem/`, {
          texto: this.novaMensagem.trim()
        })
        
        if (response.data.success) {
          this.requisicao.mensagens.push(response.data.mensagem)
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
    
    async atualizarStatus(novoStatus) {
      const acao = novoStatus === 'aceita' ? 'aceitar' : 'recusar'
      const tipo = novoStatus === 'aceita' ? 'success' : 'danger'
      
      const confirmed = await this.$confirm({
        title: `${novoStatus === 'aceita' ? 'Aceitar' : 'Recusar'} requisição`,
        message: `Tem certeza que deseja ${acao} esta requisição?`,
        type: tipo,
        confirmText: novoStatus === 'aceita' ? 'Aceitar' : 'Recusar',
        cancelText: 'Cancelar'
      })
      
      if (!confirmed) return
      
      this.atualizandoStatus = true
      
      try {
        const response = await api.post(`/api/requisicoes/${this.requisicao.id}/status/`, {
          status: novoStatus
        })
        
        if (response.data.success) {
          this.requisicao.status = novoStatus
          this.$toast.success(`Requisição ${novoStatus === 'aceita' ? 'aceita' : 'recusada'} com sucesso!`)
        }
      } catch (err) {
        console.error('Erro ao atualizar status:', err)
        this.$toast.error('Erro ao atualizar status')
      } finally {
        this.atualizandoStatus = false
      }
    },
    
    isOwnMessage(remetente) {
      // verifica se a mensagem é do usuário atual
      const userType = this.$store.getters['auth/userType']
      if (userType === 'locador' && remetente === 'locador') return true
      if (userType === 'locatario' && remetente === 'locatario') return true
      // usa valores da api se vuex não tiver
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
    
    startChatPolling() {
      // busca novas mensagens a cada 10 segundos
      this.chatPollingInterval = setInterval(() => {
        this.fetchNewMessages()
      }, 10000)
    },
    
    stopChatPolling() {
      if (this.chatPollingInterval) {
        clearInterval(this.chatPollingInterval)
        this.chatPollingInterval = null
      }
    },
    
    async fetchNewMessages() {
      if (!this.requisicao) return
      
      try {
        const response = await api.get(`/api/requisicoes/${this.requisicao.id}/`)
        
        if (response.data.success) {
          const newData = response.data.requisicao
          
          // atualiza mensagens se houver novas
          if (newData.mensagens.length !== this.requisicao.mensagens.length) {
            this.requisicao.mensagens = newData.mensagens
            this.$nextTick(() => {
              this.scrollToBottom()
            })
          }
          
          // atualiza status se mudou
          if (newData.status !== this.requisicao.status) {
            this.requisicao.status = newData.status
          }
          
          // atualiza locacaoId se foi criada uma locação (importante pro locador!)
          if (newData.locacaoId && !this.requisicao.locacaoId) {
            this.requisicao.locacaoId = newData.locacaoId
            // notifica o locador que a locação foi criada
            if (this.ehLocador) {
              this.$toast.info('O locatário realizou o pagamento! A locação foi iniciada.', 'Nova locação!')
            }
          }
          
          // atualiza outros campos
          this.requisicao.fotoDevolucao = newData.fotoDevolucao
        }
      } catch (err) {
        console.error('Erro ao buscar novas mensagens:', err)
      }
    },
    
    // === MÉTODOS DO FLUXO DE LOCAÇÃO ===
    
    async realizarPagamento() {
      const confirmed = await this.$confirm({
        title: 'Confirmar pagamento',
        message: 'Deseja confirmar o pagamento desta locação? (Simulação)',
        type: 'info',
        confirmText: 'Pagar',
        cancelText: 'Cancelar'
      })
      
      if (!confirmed) return
      
      this.processando = true
      
      try {
        const response = await api.post(`/api/requisicoes/${this.requisicao.id}/pagar/`)
        
        if (response.data.success) {
          this.$toast.success('Pagamento realizado! Locação iniciada.', 'Sucesso!')
          // Redireciona para a página da locação
          setTimeout(() => {
            this.$router.push(`/locacao/${response.data.locacao_id}`)
          }, 1500)
        } else {
          this.$toast.error(response.data.message || 'Erro ao processar pagamento')
        }
      } catch (err) {
        console.error('Erro ao pagar:', err)
        this.$toast.error(err.response?.data?.message || 'Erro ao processar pagamento')
      } finally {
        this.processando = false
      }
    }
  }
}
</script>

<style scoped>
.requisicao-detail-container {
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

/* mensagens */
.messages-container {
  height: 350px;
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

/* contato */
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

/* ==================== animacoes do chat ==================== */

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

/* cards com hover suave */
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
}

/* badge animado quando pendente */
@keyframes badgePulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.badge.bg-warning {
  animation: badgePulse 2s ease-in-out infinite;
}
</style>

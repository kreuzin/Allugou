<template>
  <div class="oferta-detail-container">
    <!-- loading state -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-danger" role="status">
        <span class="visually-hidden">carregando...</span>
      </div>
    </div>

    <!-- erro state -->
    <div v-else-if="error" class="alert alert-danger m-4">
      {{ error }}
    </div>

    <!-- conteúdo da oferta -->
    <div v-else-if="oferta" class="container-fluid p-0">
      <div class="row g-0">
        <!-- galeria de imagens -->
        <div class="col-lg-7 gallery-column">
          <div class="image-gallery">
            <!-- imagem principal -->
            <div class="main-image-container">
              <img 
                :src="getImageUrl(currentImage)" 
                :alt="oferta.titulo"
                class="main-image"
              />
              <!-- navegação da galeria -->
              <button 
                v-if="oferta.imagens.length > 1"
                @click="previousImage" 
                class="gallery-nav prev"
              >
                <i class="fa-solid fa-chevron-left"></i>
              </button>
              <button 
                v-if="oferta.imagens.length > 1"
                @click="nextImage" 
                class="gallery-nav next"
              >
                <i class="fa-solid fa-chevron-right"></i>
              </button>
            </div>
            
            <!-- miniaturas -->
            <div class="thumbnails-container" v-if="oferta.imagens.length > 1">
              <div 
                v-for="(imagem, index) in oferta.imagens" 
                :key="imagem.id"
                @click="currentImageIndex = index"
                :class="['thumbnail', { active: currentImageIndex === index }]"
              >
                <img :src="getImageUrl(imagem.imagem)" :alt="`imagem ${index + 1}`" />
              </div>
            </div>
          </div>
          
          <!-- descrição do produto -->
          <div class="description-section">
            <h3 class="description-title">Descrição do produto</h3>
            <div class="description-content">
              <p>{{ oferta.descricao }}</p>
            </div>
          </div>
        </div>

        <!-- informações da oferta -->
        <div class="col-lg-5">
          <div class="oferta-info-container">
            <!-- título e localização -->
            <div class="oferta-header">
              <h1 class="oferta-title">{{ oferta.titulo }}</h1>
              <div class="oferta-location">
                <i class="fa-solid fa-location-dot text-danger me-2"></i>
                {{ localizacao.bairro }}, {{ localizacao.cidade }} - {{ localizacao.estado }}
              </div>
            </div>

            <!-- avaliação -->
            <div class="rating-section">
              <div class="rating-stars">
                <i 
                  v-for="star in 5" 
                  :key="star"
                  :class="['fa-star', star <= averageRating ? 'fa-solid' : 'fa-regular']"
                ></i>
              </div>
              <span class="rating-text">{{ averageRating.toFixed(1) }} ({{ reviews.length }} avaliações)</span>
            </div>

            <!-- preço -->
            <div class="price-section">
              <div class="price-daily">
                <span class="price-label">diária:</span>
                <span class="price-value">R$ {{ formatPrice(oferta.valorDiaria) }}</span>
              </div>
              <div v-if="valorTotal > 0" class="price-total">
                <span class="total-label">valor total:</span>
                <span class="total-value">R$ {{ formatPrice(valorTotal) }}</span>
                <span class="total-days">({{ diasSelecionados }} {{ diasSelecionados === 1 ? 'dia' : 'dias' }})</span>
              </div>
            </div>

            <!-- entrega -->
            <div class="delivery-section">
              <div :class="['delivery-badge', { 'no-delivery': !oferta.ofereceEntrega }]">
                <i class="fa-solid fa-truck me-2"></i>
                {{ oferta.ofereceEntrega ? 'oferece entrega' : 'não oferece entrega' }}
              </div>
              
              <!-- calculadora de frete -->
              <div v-if="oferta.ofereceEntrega" class="shipping-calculator">
                <label class="shipping-label">calcular frete:</label>
                <div class="shipping-input-group">
                  <input 
                    type="text" 
                    v-model="cep"
                    @input="formatCep"
                    placeholder="00000-000"
                    maxlength="9"
                    class="form-control"
                  />
                  <button 
                    @click="calcularFrete" 
                    class="btn btn-outline-danger"
                    :disabled="!cepValido"
                  >
                    <i class="fa-solid fa-calculator me-1"></i>
                    calcular
                  </button>
                </div>
                <div v-if="freteCalculado" class="shipping-result">
                  <i class="fa-solid fa-check-circle text-success me-2"></i>
                  <span>frete: <strong>R$ {{ formatPrice(valorFrete) }}</strong></span>
                </div>
              </div>
            </div>

            <!-- calendário de seleção de datas -->
            <div class="calendar-section">
              <h3>selecione o período de locação</h3>
              <div class="date-inputs">
                <div class="form-group">
                  <label>data de início</label>
                  <input 
                    type="date" 
                    v-model="dataInicio" 
                    class="form-control"
                    :min="minDate"
                  />
                </div>
                <div class="form-group">
                  <label>data de término</label>
                  <input 
                    type="date" 
                    v-model="dataFim" 
                    class="form-control"
                    :min="dataInicio || minDate"
                  />
                </div>
              </div>

              <!-- opção de entrega/retirada -->
              <div v-if="oferta.ofereceEntrega" class="delivery-option-section">
                <label class="delivery-option-label">forma de recebimento:</label>
                <div class="form-check">
                  <input 
                    class="form-check-input" 
                    type="radio" 
                    name="deliveryOption" 
                    id="optionRetirada"
                    value="retirada"
                    v-model="opcaoEntrega"
                  >
                  <label class="form-check-label" for="optionRetirada">
                    retirar no local
                  </label>
                </div>
                <div class="form-check">
                  <input 
                    class="form-check-input" 
                    type="radio" 
                    name="deliveryOption" 
                    id="optionEntrega"
                    value="entrega"
                    v-model="opcaoEntrega"
                  >
                  <label class="form-check-label" for="optionEntrega">
                    solicitar entrega
                    <span v-if="freteCalculado" class="text-success ms-2">
                      (+ R$ {{ formatPrice(valorFrete) }})
                    </span>
                  </label>
                </div>
              </div>
              
              <!-- resumo do período -->
              <div v-if="dataInicio && dataFim" class="rental-summary">
                <div class="summary-row">
                  <span>período:</span>
                  <span>{{ diasSelecionados }} {{ diasSelecionados === 1 ? 'dia' : 'dias' }}</span>
                </div>
                <div class="summary-row">
                  <span>valor da diária:</span>
                  <span>R$ {{ formatPrice(oferta.valorDiaria) }}</span>
                </div>
                <div class="summary-row">
                  <span>subtotal:</span>
                  <span>R$ {{ formatPrice(valorTotal) }}</span>
                </div>
                <div v-if="opcaoEntrega === 'entrega' && freteCalculado" class="summary-row">
                  <span>frete:</span>
                  <span>R$ {{ formatPrice(valorFrete) }}</span>
                </div>
                <div class="summary-row total">
                  <span>total:</span>
                  <span>R$ {{ formatPrice(valorTotalComFrete) }}</span>
                </div>
              </div>

              <button 
                @click="solicitarLocacao"
                class="btn btn-danger btn-lg w-100 mt-3" 
                :disabled="!podeRequisitar"
              >
                {{ botaoText }}
              </button>
            </div>

            <!-- informações do locador -->
            <div class="locador-section">
              <h3>Anunciante</h3>
              <div class="locador-info">
                <i class="fa-solid fa-user-circle fa-2x text-secondary me-3"></i>
                <div>
                  <div class="locador-name">{{ locador.nome }}</div>
                  <div class="locador-username">@{{ locador.user }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- avaliações -->
      <div class="reviews-section container py-4">
        <h2 class="mb-4">Avaliações</h2>
        
        <div class="row">
          <div v-for="review in reviews" :key="review.id" class="col-md-6 mb-4">
            <div class="review-card">
              <div class="review-header">
                <div class="review-author">
                  <i class="fa-solid fa-user-circle fa-2x text-secondary me-2"></i>
                  <div>
                    <div class="author-name">{{ review.author }}</div>
                    <div class="review-date">{{ review.date }}</div>
                  </div>
                </div>
                <div class="review-stars">
                  <i 
                    v-for="star in 5" 
                    :key="star"
                    :class="['fa-star', 'fa-sm', star <= review.rating ? 'fa-solid' : 'fa-regular']"
                  ></i>
                </div>
              </div>
              <p class="review-text">{{ review.text }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- modal de confirmação -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>confirmar solicitação de locação</h3>
          <button @click="showModal = false" class="close-btn">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="summary-item">
            <strong>produto:</strong>
            <span>{{ oferta.titulo }}</span>
          </div>
          
          <div class="summary-item">
            <strong>período:</strong>
            <span>{{ formatDate(dataInicio) }} até {{ formatDate(dataFim) }} ({{ diasSelecionados }} {{ diasSelecionados === 1 ? 'dia' : 'dias' }})</span>
          </div>
          
          <div class="summary-item">
            <strong>valor da diária:</strong>
            <span>R$ {{ formatPrice(oferta.valorDiaria) }}</span>
          </div>
          
          <div class="summary-item">
            <strong>subtotal:</strong>
            <span>R$ {{ formatPrice(valorTotal) }}</span>
          </div>
          
          <div v-if="opcaoEntrega === 'entrega'" class="summary-item">
            <strong>forma de recebimento:</strong>
            <span>entrega no endereço</span>
          </div>
          <div v-else class="summary-item">
            <strong>forma de recebimento:</strong>
            <span>retirada no local</span>
          </div>
          
          <div v-if="opcaoEntrega === 'entrega' && freteCalculado" class="summary-item">
            <strong>frete:</strong>
            <span>R$ {{ formatPrice(valorFrete) }}</span>
          </div>
          
          <div class="summary-item total-item">
            <strong>total:</strong>
            <span class="total-value">R$ {{ formatPrice(valorTotalComFrete) }}</span>
          </div>
          
          <div class="summary-item">
            <strong>anunciante:</strong>
            <span>{{ locador.nome }} (@{{ locador.user }})</span>
          </div>

          <!-- endereço do locatário -->
          <div v-if="enderecoLocatario" class="summary-item">
            <strong>seu endereço:</strong>
            <span>{{ enderecoLocatario.rua }}, {{ enderecoLocatario.numero }} - {{ enderecoLocatario.bairro }}, {{ enderecoLocatario.cidade }}/{{ enderecoLocatario.estado }}</span>
          </div>

          <!-- contrato de responsabilidades -->
          <div class="contrato-section">
            <h4>Termos e Responsabilidades</h4>
            <div class="contrato-texto">
              <p><strong>Ao confirmar esta solicitação, você concorda com os seguintes termos:</strong></p>
              <ul>
                <li>O locatário se compromete a utilizar o item de forma adequada e devolvê-lo nas mesmas condições em que o recebeu.</li>
                <li>O locatário é responsável por quaisquer danos causados ao item durante o período de locação.</li>
                <li>O locador se compromete a entregar o item nas condições descritas no anúncio.</li>
                <li>O pagamento deve ser realizado antes da retirada/entrega do item.</li>
                <li>Em caso de atraso na devolução, poderão ser cobradas diárias adicionais.</li>
                <li>Ambas as partes concordam em resolver eventuais conflitos de forma amigável.</li>
              </ul>
              <p class="contrato-disclaimer"><em>[Este é um contrato simplificado para fins de protótipo. Um contrato completo será elaborado pelo time legal.]</em></p>
            </div>
            <div class="form-check mt-3">
              <input 
                class="form-check-input" 
                type="checkbox" 
                id="aceitarTermos"
                v-model="aceitouTermos"
              >
              <label class="form-check-label" for="aceitarTermos">
                Li e aceito os termos e responsabilidades acima
              </label>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showModal = false" class="btn btn-secondary">
            cancelar
          </button>
          <button @click="confirmarRequisicao" class="btn btn-danger" :disabled="enviando">
            <span v-if="enviando">
              <i class="fa-solid fa-spinner fa-spin me-2"></i>
              processando...
            </span>
            <span v-else>
              confirmar solicitação
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'OfertaDetailView',
  data() {
    return {
      oferta: null,
      locador: null,
      localizacao: null,
      enderecoLocatario: null,
      loading: true,
      error: null,
      currentImageIndex: 0,
      dataInicio: null,
      dataFim: null,
      cep: '',
      freteCalculado: false,
      valorFrete: 0,
      opcaoEntrega: 'retirada',
      showModal: false,
      enviando: false,
      aceitouTermos: false,
      // reviews de placeholder
      reviews: [
        {
          id: 1,
          author: 'João Silva',
          date: '15/11/2025',
          rating: 5,
          text: 'Excelente produto! Muito bem conservado e o locador foi super atencioso. Recomendo!'
        },
        {
          id: 2,
          author: 'Maria Santos',
          date: '10/11/2025',
          rating: 4,
          text: 'Ótima experiência. O item estava em bom estado e a entrega foi pontual.'
        },
        {
          id: 3,
          author: 'Pedro Costa',
          date: '05/11/2025',
          rating: 5,
          text: 'Perfeito! Atendeu todas as minhas expectativas. Com certeza alugarei novamente.'
        },
        {
          id: 4,
          author: 'Ana Oliveira',
          date: '01/11/2025',
          rating: 3,
          text: 'Bom no geral, mas poderia estar um pouco mais limpo. Fora isso, tudo certo.'
        },
        {
          id: 5,
          author: 'Carlos Mendes',
          date: '28/10/2025',
          rating: 5,
          text: 'Produto de qualidade e atendimento nota 10. Super recomendo!'
        },
        {
          id: 6,
          author: 'Juliana Lima',
          date: '22/10/2025',
          rating: 4,
          text: 'Muito bom! Só não dou 5 estrelas porque a devolução poderia ser mais flexível.'
        }
      ]
    }
  },
  computed: {
    currentImage() {
      return this.oferta?.imagens[this.currentImageIndex]?.imagem || ''
    },
    averageRating() {
      if (this.reviews.length === 0) return 0
      const sum = this.reviews.reduce((acc, review) => acc + review.rating, 0)
      return sum / this.reviews.length
    },
    minDate() {
      return new Date().toISOString().split('T')[0]
    },
    diasSelecionados() {
      if (!this.dataInicio || !this.dataFim) return 0
      const inicio = new Date(this.dataInicio)
      const fim = new Date(this.dataFim)
      const diffTime = Math.abs(fim - inicio)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      return diffDays + 1 // incluir o último dia
    },
    valorTotal() {
      return this.diasSelecionados * this.oferta.valorDiaria
    }
  },
  async mounted() {
    await this.loadOferta()
  },
  methods: {
    async loadOferta() {
      try {
        this.loading = true
        const ofertaId = this.$route.params.id
        const response = await api.get(`/api/ofertas/${ofertaId}/`)
        
        if (response.data.success) {
          this.oferta = response.data.oferta
          this.locador = response.data.locador
          this.localizacao = response.data.localizacao
          
          // ordenar imagens: principal primeiro
          this.oferta.imagens.sort((a, b) => {
            if (a.ehImagemPrincipal) return -1
            if (b.ehImagemPrincipal) return 1
            return a.ordem - b.ordem
          })
        } else {
          this.error = response.data.message
        }
      } catch (err) {
        this.error = 'erro ao carregar oferta. tente novamente.'
        console.error('erro:', err)
      } finally {
        this.loading = false
      }
    },
    getImageUrl(imagePath) {
      if (!imagePath) return ''
      return `http://localhost:8000${imagePath}`
    },
    formatPrice(value) {
      return parseFloat(value).toFixed(2).replace('.', ',')
    },
    nextImage() {
      if (this.currentImageIndex < this.oferta.imagens.length - 1) {
        this.currentImageIndex++
      } else {
        this.currentImageIndex = 0
      }
    },
    previousImage() {
      if (this.currentImageIndex > 0) {
        this.currentImageIndex--
      } else {
        this.currentImageIndex = this.oferta.imagens.length - 1
      }
    },
    formatCep(event) {
      let value = event.target.value.replace(/\D/g, '')
      if (value.length > 5) {
        value = value.slice(0, 5) + '-' + value.slice(5, 8)
      }
      this.cep = value
    },
    calcularFrete() {
      // simulação de cálculo de frete
      if (this.cepValido) {
        // valor fake entre 15 e 50 reais
        this.valorFrete = (Math.random() * 35 + 15).toFixed(2)
        this.freteCalculado = true
      }
    },
    solicitarLocacao() {
      if (this.podeRequisitar) {
        this.aceitouTermos = false
        this.fetchEnderecoLocatario()
        this.showModal = true
      }
    },
    async fetchEnderecoLocatario() {
      try {
        const response = await api.get('/api/meu-endereco/')
        if (response.data.success) {
          this.enderecoLocatario = response.data.endereco
        }
      } catch (error) {
        console.error('erro ao buscar endereço:', error)
      }
    },
    async confirmarRequisicao() {
      if (!this.aceitouTermos) {
        this.$toast.warning('Você precisa aceitar os termos e responsabilidades para continuar.')
        return
      }
      
      try {
        this.enviando = true
        
        const requisicaoData = {
          oferta_id: this.oferta.id,
          data_inicio: this.dataInicio,
          data_fim: this.dataFim,
          opcao_entrega: this.opcaoEntrega,
          valor_frete: this.opcaoEntrega === 'entrega' ? this.valorFrete : 0,
          valor_total: this.valorTotalComFrete
        }
        
        const response = await api.post('/api/requisicoes/create/', requisicaoData)
        
        if (response.data.success) {
          this.showModal = false
          this.$toast.success('Solicitação enviada com sucesso! O locador receberá sua requisição.', 'Requisição enviada!')
          // redirecionar para home ou página de requisições
          setTimeout(() => {
            this.$router.push('/')
          }, 1500)
        } else {
          throw new Error(response.data.message || 'erro ao criar requisição')
        }
        
      } catch (error) {
        console.error('erro ao criar requisição:', error)
        this.$toast.error('Erro ao enviar solicitação. Tente novamente.')
      } finally {
        this.enviando = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString + 'T00:00:00')
      return date.toLocaleDateString('pt-BR')
    }
  },
  computed: {
    currentImage() {
      return this.oferta?.imagens[this.currentImageIndex]?.imagem || ''
    },
    averageRating() {
      if (this.reviews.length === 0) return 0
      const sum = this.reviews.reduce((acc, review) => acc + review.rating, 0)
      return sum / this.reviews.length
    },
    minDate() {
      return new Date().toISOString().split('T')[0]
    },
    diasSelecionados() {
      if (!this.dataInicio || !this.dataFim) return 0
      const inicio = new Date(this.dataInicio)
      const fim = new Date(this.dataFim)
      const diffTime = Math.abs(fim - inicio)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      return diffDays + 1 // incluir o último dia
    },
    valorTotal() {
      return this.diasSelecionados * this.oferta.valorDiaria
    },
    valorTotalComFrete() {
      let total = this.valorTotal
      if (this.opcaoEntrega === 'entrega' && this.freteCalculado) {
        total += parseFloat(this.valorFrete)
      }
      return total
    },
    cepValido() {
      return this.cep.replace(/\D/g, '').length === 8
    },
    isLocatario() {
      return this.$store.getters['auth/isAuthenticated'] && 
             this.$store.state.auth.userType === 'locatario'
    },
    isAuthenticated() {
      return this.$store.getters['auth/isAuthenticated']
    },
    podeRequisitar() {
      if (!this.isAuthenticated) return false
      if (!this.isLocatario) return false
      if (!this.dataInicio || !this.dataFim) return false
      if (!this.oferta.ofereceEntrega) return true
      if (this.opcaoEntrega === 'retirada') return true
      return this.opcaoEntrega === 'entrega' && this.freteCalculado
    },
    botaoText() {
      if (!this.isAuthenticated) return 'faça login para solicitar'
      if (!this.isLocatario) return 'disponível apenas para locatários'
      if (!this.dataInicio || !this.dataFim) return 'selecione as datas'
      if (this.oferta.ofereceEntrega && this.opcaoEntrega === 'entrega' && !this.freteCalculado) {
        return 'calcule o frete primeiro'
      }
      return 'solicitar locação'
    }
  }
}
</script>

<style scoped>
.oferta-detail-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* coluna da galeria centralizada verticalmente */
.gallery-column {
  align-self: center;
}

/* galeria de imagens */
.image-gallery {
  background-color: #000;
}

/* descrição dentro da coluna da galeria */
.description-section {
  background-color: #fff;
  padding: 25px 30px;
  border-top: 1px solid #e5e7eb;
}

.description-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 15px;
}

.description-section .description-content {
  background-color: #f9fafb;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.description-section .description-content p {
  color: #374151;
  line-height: 1.7;
  font-size: 0.95rem;
  margin: 0;
  white-space: pre-wrap;
}

.main-image-container {
  position: relative;
  width: 100%;
  height: 500px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background-color: #000;
}

.gallery-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s;
  z-index: 10;
}

.gallery-nav:hover {
  background-color: rgba(255, 255, 255, 1);
}

.gallery-nav.prev {
  left: 20px;
}

.gallery-nav.next {
  right: 20px;
}

.thumbnails-container {
  display: flex;
  gap: 10px;
  padding: 15px;
  overflow-x: auto;
  background-color: #1a1a1a;
}

.thumbnail {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 4px;
  overflow: hidden;
  transition: border-color 0.3s;
}

.thumbnail:hover,
.thumbnail.active {
  border-color: #dc3545;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* informações da oferta */
.oferta-info-container {
  padding: 30px;
  background-color: #fff;
}

.oferta-header {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #dee2e6;
}

.oferta-title {
  font-size: 2rem;
  font-weight: bold;
  color: #212529;
  margin-bottom: 10px;
}

.oferta-location {
  color: #6c757d;
  font-size: 1rem;
}

.rating-section {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.rating-stars i {
  color: #ffc107;
  font-size: 1.2rem;
}

.rating-text {
  color: #6c757d;
  font-size: 0.95rem;
}

.price-section {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.price-daily {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #dee2e6;
}

.price-label {
  color: #6c757d;
  font-size: 0.9rem;
  display: block;
  margin-bottom: 5px;
}

.price-value {
  color: #dc3545;
  font-size: 2rem;
  font-weight: bold;
}

.price-total {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.total-label {
  color: #495057;
  font-size: 0.95rem;
  font-weight: 500;
}

.total-value {
  color: #28a745;
  font-size: 1.8rem;
  font-weight: bold;
}

.total-days {
  color: #6c757d;
  font-size: 0.85rem;
}

/* entrega e frete */
.delivery-section {
  margin-bottom: 20px;
}

.delivery-badge {
  display: inline-flex;
  align-items: center;
  background-color: #d4edda;
  color: #155724;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  margin-bottom: 15px;
}

.delivery-badge.no-delivery {
  background-color: #e9ecef;
  color: #6c757d;
}

.shipping-calculator {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.shipping-label {
  display: block;
  font-size: 0.9rem;
  color: #495057;
  font-weight: 500;
  margin-bottom: 10px;
}

.shipping-input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.shipping-input-group input {
  flex: 1;
}

.shipping-input-group button {
  white-space: nowrap;
}

.shipping-result {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #d4edda;
  border-radius: 6px;
  color: #155724;
  font-size: 0.95rem;
}

/* calendário */
.calendar-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.calendar-section h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #212529;
}

.date-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 5px;
}

.rental-summary {
  margin-top: 15px;
  padding: 15px;
  background-color: #fff;
  border-radius: 4px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 0.95rem;
}

.summary-row.total {
  border-top: 2px solid #dee2e6;
  margin-top: 10px;
  padding-top: 15px;
  font-weight: bold;
  font-size: 1.1rem;
  color: #dc3545;
}

/* opções de entrega */
.delivery-option-section {
  margin: 15px 0;
  padding: 15px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #dee2e6;
}

.delivery-option-label {
  display: block;
  font-size: 0.9rem;
  color: #495057;
  font-weight: 500;
  margin-bottom: 10px;
}

.form-check {
  padding-left: 1.5rem;
  margin-bottom: 8px;
}

.form-check-input:checked {
  background-color: #dc3545;
  border-color: #dc3545;
}

/* modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.modal-content {
  background-color: #fff;
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #212529;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6c757d;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #f8f9fa;
  color: #212529;
}

.modal-body {
  padding: 25px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f1f3f5;
  font-size: 0.95rem;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-item strong {
  color: #495057;
  font-weight: 500;
}

.summary-item span {
  color: #212529;
  text-align: right;
  max-width: 60%;
}

.summary-item.total-item {
  margin-top: 15px;
  padding-top: 20px;
  border-top: 2px solid #dee2e6;
  border-bottom: none;
  font-size: 1.1rem;
}

.summary-item.total-item strong {
  font-weight: 600;
  color: #212529;
}

.summary-item.total-item .total-value {
  color: #dc3545;
  font-weight: bold;
  font-size: 1.3rem;
}

/* contrato de responsabilidades */
.contrato-section {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.contrato-section h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 15px;
}

.contrato-texto {
  font-size: 0.9rem;
  color: #495057;
  max-height: 200px;
  overflow-y: auto;
  padding: 15px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

.contrato-texto ul {
  margin: 10px 0;
  padding-left: 20px;
}

.contrato-texto li {
  margin-bottom: 8px;
  line-height: 1.5;
}

.contrato-disclaimer {
  margin-top: 15px;
  font-size: 0.85rem;
  color: #6c757d;
}

.modal-footer {
  padding: 20px 25px;
  border-top: 1px solid #dee2e6;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.modal-footer .btn {
  padding: 10px 20px;
  font-weight: 500;
}

/* locador */
.locador-section {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.locador-section h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #212529;
}

.locador-info {
  display: flex;
  align-items: center;
}

.locador-name {
  font-weight: 600;
  color: #212529;
}

.locador-username {
  color: #6c757d;
  font-size: 0.9rem;
}

/* avaliações */
.reviews-section {
  background-color: #fff;
}

.reviews-section h2 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #212529;
}

.review-card {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  height: 100%;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.review-author {
  display: flex;
  align-items: center;
}

.author-name {
  font-weight: 600;
  color: #212529;
}

.review-date {
  color: #6c757d;
  font-size: 0.85rem;
}

.review-stars i {
  color: #ffc107;
}

.review-text {
  color: #495057;
  line-height: 1.6;
  margin: 0;
}

/* responsivo */
@media (max-width: 991px) {
  .main-image-container {
    height: 400px;
  }
  
  .oferta-info-container {
    max-height: none;
  }
}

@media (max-width: 576px) {
  .date-inputs {
    grid-template-columns: 1fr;
  }
  
  .oferta-title {
    font-size: 1.5rem;
  }
}
</style>

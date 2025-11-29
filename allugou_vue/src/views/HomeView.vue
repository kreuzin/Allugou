<template>
  <div class="home-view">
    <HomeHero :categories="categories" />
    
    <section class="products-section py-5">
      <div class="section-header-wrapper">
        <div class="container">
          <h2 class="section-title mb-4">Ofertas de locação</h2>
        </div>
      </div>

      <div class="container">
        <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>

        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Carregando...</span>
          </div>
        </div>
        
        <div v-else class="products-grid">
          <ProductCard 
            v-for="(product, index) in products" 
            :key="product.id" 
            :product="product"
            class="product-card-animated"
            :style="{ '--card-index': index }"
            @open="handleProductClick"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import HomeHero from '@/components/HomeHero.vue'
import ProductCard from '@/components/ProductCard.vue'
import { ofertaLocacaoService, getMediaUrl } from '@/services/api'

export default {
  name: 'HomeView',
  components: {
    HomeHero,
    ProductCard
  },
  data: () => ({
    categories: [
      'Cadeiras de festa',
      'Camera fotográfica',
      'Caixa de som',
      'Máquina de fliperama',
      'Nível a Laser',
      'Cama elástica',
      'Trena'
    ],
    products: [],
    loading: false,
    error: null
  }),
  created() {
    this.fetchOfertas()
  },
  methods: {
    async fetchOfertas() {
      this.loading = true
      this.error = null
      try {
        const response = await ofertaLocacaoService.getAllOfertas()
        
        if (!response || !response.data) {
          throw new Error('nenhum dado recebido')
        }

        // verificar se a resposta é paginada ou uma matriz direta
        let ofertas = []
        if (response.data.success && response.data.ofertas) {
          ofertas = response.data.ofertas
        } else if (Array.isArray(response.data)) {
          ofertas = response.data
        } else if (response.data.results) {
          ofertas = response.data.results
        }
        
        if (ofertas.length === 0) {
          this.error = 'nenhuma oferta encontrada.'
          return
        }
        
        this.products = ofertas.map(oferta => {
          // extrair localização
          let location = oferta.localizacao_completa || 'localização não informada'

          // obter URL da imagem principal ou primeira disponível
          let imageUrl = 'https://via.placeholder.com/800x600?text=Sem+Imagem'
          if (oferta.imagem_principal && oferta.imagem_principal.imagem) {
            imageUrl = getMediaUrl(oferta.imagem_principal.imagem)
          } else if (oferta.imagens && oferta.imagens.length > 0) {
            imageUrl = getMediaUrl(oferta.imagens[0].imagem)
          }

          return {
            id: oferta.id,
            title: oferta.titulo || 'sem título',
            subtitle: oferta.descricao || 'sem descrição',
            price: oferta.valorDiaria ? `R$${oferta.valorDiaria.toFixed(2)}` : 'preço não informado',
            per: 'por dia',
            location: location,
            image: imageUrl,
            ofereceEntrega: oferta.ofereceEntrega || false
          }
        })
        
      } catch (error) {
        console.error('erro ao buscar ofertas:', error)
        this.error = 'erro ao carregar as ofertas. por favor, tente novamente.'
      } finally {
        this.loading = false
      }
    },
    handleProductClick(product) {
      // navegar para página de detalhes
      this.$router.push(`/oferta/${product.id}`)
    }
  }
}
</script>

<style scoped>
.home-view {
  background: #fff;
}

/* cabeçalho de seção com linha horizontal de largura total */
.section-header-wrapper {
  position: relative;
  width: 100%;
  padding: 1rem 0 0.5rem; /* espaço ao redor do título */
}
.section-header-wrapper::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 2px;
  background: linear-gradient(90deg, rgba(0,0,0,0.08), rgba(0,0,0,0.12));
  transform: translateY(-50%);
  z-index: 0;
}
.section-header-wrapper .container {
  position: relative;
  z-index: 1; /* manter título acima da linha */
  display: flex;
  justify-content: center;
}
.section-title {
  display: inline-block;
  margin: 0;
  padding: 0 1rem;
  background: #f8f9fa; /* mascarar a linha horizontal atrás do título */
  font-size: 1.75rem;
  font-weight: 700;
  color: #2d3436;
  text-align: center;
  white-space: nowrap;
}

.products-section {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  padding-top: 0; /* o wrapper do cabeçalho lida com o preenchimento superior */
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 0.5rem 0;
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
}

/* ==================== ANIMAÇÕES DOS CARDS ==================== */

/* Cards entrando com stagger */
.product-card-animated {
  animation: cardIn 0.5s ease-out backwards;
  animation-delay: calc(var(--card-index, 0) * 0.08s);
}

@keyframes cardIn {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Spinner com animação suave */
.spinner-border {
  color: #00897b;
}
</style>
<template>
  <div class="home-view">
    <HomeHero :categories="categories" />
    
    <section class="products-section py-5">
      <div class="container">
        <h2 class="section-title mb-4">Ofertas de locação</h2>
        
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
            v-for="product in products" 
            :key="product.id" 
            :product="product"
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
      console.log('Starting fetchOfertas')
      this.loading = true
      this.error = null
      try {
        console.log('Making API request...')
        const response = await ofertaLocacaoService.getAllOfertas()
        console.log('Raw response:', response)
        
        if (!response || !response.data) {
          throw new Error('No response data received')
        }

        // Check if the response is paginated or direct array
        let ofertas = []
        if (Array.isArray(response.data)) {
          console.log('Response is an array')
          ofertas = response.data
        } else if (response.data.results) {
          console.log('Response is paginated')
          ofertas = response.data.results
        } else {
          console.log('Response data:', response.data)
          throw new Error('Unexpected response format')
        }

        console.log('Ofertas array:', ofertas)
        console.log('Number of ofertas:', ofertas.length)
        
        if (ofertas.length === 0) {
          console.log('No ofertas found in the response')
          this.error = 'Nenhuma oferta encontrada.'
          return
        }
        
        this.products = ofertas.map(oferta => {
          console.log('Processing individual oferta:', oferta)
          
          // Extract location from nested data
          let location = 'Localização não informada'
          if (oferta.locador && oferta.locador.endereco) {
            const endereco = oferta.locador.endereco
            location = `${endereco.cidade}${endereco.estado ? ` - ${endereco.estado}` : ''}`
          }

          // Get image URL from the main image or first available image
          let imageUrl = 'https://via.placeholder.com/800x600?text=Sem+Imagem'
          if (oferta.imagem_principal && oferta.imagem_principal.imagem) {
            imageUrl = getMediaUrl(oferta.imagem_principal.imagem)
          } else if (oferta.imagens && oferta.imagens.length > 0) {
            imageUrl = getMediaUrl(oferta.imagens[0].imagem)
          }

          const mapped = {
            id: oferta.id,
            title: oferta.titulo || 'Sem título',
            subtitle: oferta.descricao || 'Sem descrição',
            price: oferta.valorDiaria ? `R$${oferta.valorDiaria.toFixed(2)}` : 'Preço não informado',
            per: 'por dia',
            location: location,
            image: imageUrl,
            ofereceEntrega: oferta.ofereceEntrega || false,
            rawData: oferta // Keep raw data for debugging
          }
          console.log('Mapped product:', mapped)
          return mapped
        })

        console.log('Products after mapping:', this.products)
        
      } catch (error) {
        console.error('Error fetching ofertas:', error)
        this.error = 'Erro ao carregar as ofertas. Por favor, tente novamente.'
      } finally {
        this.loading = false
      }
    },
    handleProductClick(product) {
      console.log('Product clicked:', product)
      // TODO: Navigate to product detail or show modal
    }
  }
}
</script>

<style scoped>
.home-view {
  background: #fff;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2d3436;
}

.products-section {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
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
</style>
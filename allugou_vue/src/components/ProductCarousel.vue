<template>
  <section class="product-carousel py-5">
    <div class="container">
      <div class="d-flex align-items-center justify-content-between mb-4">
        <h2 class="section-title m-0">Ferramentas para construção civil</h2>
        <div class="nav-buttons">
          <button class="btn btn-nav" @click="scroll(-300)">
            <i class="fas fa-chevron-left"></i>
          </button>
          <button class="btn btn-nav" @click="scroll(300)">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
      
      <div class="carousel-wrapper position-relative">
        <div ref="track" class="track d-flex py-2">
          <ProductCard v-for="(p, i) in products" :key="i" :product="p" @open="onOpen" />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import ProductCard from './ProductCard.vue'

export default {
  name: 'ProductCarousel',
  components: { ProductCard },
  props: {
    products: { type: Array, default: () => [] }
  },
  methods: {
    scroll (delta) {
      this.$refs.track.scrollBy({ left: delta, behavior: 'smooth' })
    },
    onOpen (product) {
      this.$emit('open', product)
    }
  }
}
</script>

<style scoped>
.product-carousel {
  background-color: #f8f9fa;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2d3436;
}

.nav-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-nav {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  border: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-nav:hover {
  background: #00897b;
  border-color: #00897b;
  color: white;
}

.track {
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0.5rem 0 1.5rem;
  margin: 0 -0.5rem;
}

/* Hide scrollbar but keep functionality */
.track {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
}

.track::-webkit-scrollbar {
  display: none; /* Chrome/Safari/Opera */
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.5rem;
  }
  
  .nav-buttons {
    display: none;
  }
}
</style>

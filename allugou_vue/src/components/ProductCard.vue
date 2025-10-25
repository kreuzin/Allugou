<template>
  <a href="#" class="product-card" @click.prevent="open">
    <div class="card shadow-sm h-100">
      <div class="card-img-wrapper">
        <img :src="product.image" class="card-img-top" :alt="product.title"/>
      </div>
      <div class="card-body d-flex flex-column">
        <h5 class="card-title text-truncate">{{ product.title }}</h5>
        <p class="card-text text-muted small mb-3">{{ product.subtitle }}</p>
        <div class="mt-auto">
          <div class="mb-2">
            <strong class="price h5 mb-0">{{ product.price }}</strong>
            <small class="text-muted ms-2">{{ product.per }}</small>
          </div>
          <div class="location mb-2">
            <i class="fas fa-map-marker-alt text-muted me-1"></i>
            <small class="text-muted">{{ product.location }}</small>
          </div>
          <div v-if="product.ofereceEntrega" class="delivery">
            <i class="fas fa-truck text-success me-1"></i>
            <small class="text-success">Entrega disponível</small>
          </div>
        </div>
      </div>
    </div>
  </a>
</template>

<script>
export default {
  name: 'ProductCard',
  props: {
    product: { type: Object, required: true }
  },
  methods: {
    open () {
      this.$emit('open', this.product)
    }
  }
}
</script>

<style scoped>
.product-card {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 250px;
  margin-right: 1rem;
  transition: transform 0.2s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  text-decoration: none;
  color: inherit;
}

.card {
  border-radius: 12px;
  border: none;
  background: white;
}

.card-img-wrapper {
  height: 160px;
  overflow: hidden;
  border-radius: 12px 12px 0 0;
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .card-img-top {
  transform: scale(1.05);
}

.card-body {
  padding: 1.25rem;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2d3436;
}

.price {
  color: #00897b;
  font-size: 1.25rem;
}

.location {
  font-size: 0.875rem;
}

.shadow-sm {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
}
</style>

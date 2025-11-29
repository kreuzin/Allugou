<template>
  <a href="#" class="product-card" @click.prevent="open">
    <div class="card shadow-sm h-100">
      <div class="card-img-wrapper">
        <img :src="product.image" class="card-img-top" :alt="product.title"/>
      </div>
      <div class="card-body d-flex flex-column">
        <h5 class="card-title text-truncate">{{ product.title }}</h5>
        <p class="card-text text-muted small mb-3 description-truncate">{{ product.subtitle }}</p>
        <div class="mt-auto">
          <div class="mb-2">
            <strong class="price h5 mb-0">{{ product.price }}</strong>
            <small class="text-muted ms-2">{{ product.per }}</small>
          </div>
          <div class="location mb-2">
            <i class="fas fa-map-marker-alt text-muted me-1"></i>
            <small class="text-muted">{{ product.location }}</small>
          </div>
          <div class="delivery">
            <i :class="['fas fa-truck me-1', product.ofereceEntrega ? 'text-success' : 'text-secondary']"></i>
            <small :class="product.ofereceEntrega ? 'text-success' : 'text-secondary'">
              {{ product.ofereceEntrega ? 'Entrega disponível' : 'Sem entrega' }}
            </small>
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
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover {
  transform: translateY(-8px);
  text-decoration: none;
  color: inherit;
}

.card {
  border-radius: 12px;
  border: none;
  background: white;
  transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover .card {
  box-shadow: 0 12px 40px rgba(0,0,0,0.15) !important;
}

.card-img-wrapper {
  height: 160px;
  overflow: hidden;
  border-radius: 12px 12px 0 0;
  position: relative;
}

/* overlay no hover */
.card-img-wrapper::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.product-card:hover .card-img-wrapper::after {
  opacity: 1;
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover .card-img-top {
  transform: scale(1.08);
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

.description-truncate {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
  max-height: 2.8em;
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

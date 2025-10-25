<template>
  <div class="category-chips">
    <h2 class="mb-4">Aqui temos:</h2>
    <div class="chips-container">
      <button v-for="(c, i) in categories" :key="i" class="btn btn-outline-teal chip">{{ c }}</button>
    </div>

    <a class="link-more mt-4" href="#">E muito mais...</a>
  </div>
</template>

<script>
export default {
  name: 'CategoryChips',
  props: {
    categories: {
      type: Array,
      default: () => [
        'Cadeiras de festa',
        'Camera fotográfica',
        'Caixa de som',
        'Máquina de fliperama',
        'Nível a Laser',
        'Cama elástica',
        'Trena'
      ]
    }
  }
}
</script>

<style scoped>
.category-chips {
  padding: 1rem 0;
}

.category-chips h2 {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 1.5rem;
  letter-spacing: -0.5px;
}

.chips-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.chip {
  border-radius: 50px;
  padding: 0.625rem 1.25rem;
  font-weight: 500;
  font-size: 0.95rem;
  border: 2px solid #46efb1;
  color: #13e9bf;
  background: transparent;
  transition: all 0.2s ease;
}

.chip:hover {
  background-color: #26a69a;
  color: white;
  border-color: #26a69a;
}

.link-more {
  display: block;
  color: #00c29b;
  font-weight: 500;
  font-size: 0.95rem;
  text-decoration: none;
  margin-top: 1.25rem;
}

.link-more:hover {
  color: #15d9c2;
  text-decoration: underline;
}
</style>

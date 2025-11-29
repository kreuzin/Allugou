<template>
  <div class="home-hero-section py-4">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-4">
          <CategoryChips :categories="categories" />
        </div>
        <div class="col-md-8">
          <div class="simple-carousel">
            <div class="carousel-container">
              <transition-group name="fade" tag="div" class="images-wrapper">
                <img 
                  v-for="(img, idx) in images" 
                  :key="img"
                  v-show="currentIndex === idx"
                  :src="img" 
                  :alt="`slide-${idx}`"
                  class="carousel-image"
                />
              </transition-group>
              
              <button class="nav-btn prev" @click="prev" aria-label="Previous image">
                <i class="fas fa-chevron-left"></i>
              </button>
              <button class="nav-btn next" @click="next" aria-label="Next image">
                <i class="fas fa-chevron-right"></i>
              </button>

              <div class="indicators">
                <button 
                  v-for="(_, idx) in images" 
                  :key="idx"
                  :class="['indicator', { active: currentIndex === idx }]"
                  @click="goToSlide(idx)"
                  :aria-label="`Go to slide ${idx + 1}`"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CategoryChips from './CategoryChips.vue'

export default {
  name: 'HomeHero',
  components: { CategoryChips },
  props: {
    categories: { type: Array, default: () => [] }
  },
  data() {
    return {
      images: [
        'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=1400&q=80',
        'https://images.unsplash.com/photo-1542038784456-1ea8e935640e?auto=format&fit=crop&w=1400&q=80',
      ],
      currentIndex: 0,
      timer: null
    }
  },
  mounted() {
    this.startTimer()
  },
  beforeDestroy() {
    this.stopTimer()
  },
  methods: {
    startTimer() {
      this.stopTimer()
      this.timer = setInterval(this.next, 5000)
    },
    stopTimer() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    },
    next() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length
    },
    prev() {
      this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length
    },
    goToSlide(index) {
      this.currentIndex = index
      this.startTimer() // reseta o timer ao apertar o botaozin de mudar slide
    }
  }
}
</script>

<style scoped>
.home-hero-section {
  background: linear-gradient(to right, #001a13, #004d40);
}

.simple-carousel {
  position: relative;
  border-radius: 18px;
  overflow: hidden;
}

.carousel-container {
  position: relative;
  width: 100%;
  height: 300px;
  border-radius: 18px;
  overflow: hidden;
}

.images-wrapper {
  height: 100%;
  width: 100%;
}

.carousel-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 18px;
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 2;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.5);
}

.prev {
  left: 16px;
}

.next {
  right: 16px;
}

.indicators {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 2;
}

.indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 0;
  transition: all 0.3s ease;
}

.indicator.active {
  background: white;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .carousel-container {
    height: 200px;
  }

  .nav-btn {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
}
</style>

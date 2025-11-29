<!-- toast notification é aquele quadradinho que aparece no canto da tela quando alguma ação acontece, tipo sucesso, erro, aviso, etc -->

<template>
  <transition-group name="toast" tag="div" class="toast-container">
    <div 
      v-for="toast in toasts" 
      :key="toast.id"
      class="toast-item"
      :class="'toast-' + toast.type"
    >
      <div class="toast-icon">
        <i :class="getIcon(toast.type)"></i>
      </div>
      <div class="toast-content">
        <div class="toast-title" v-if="toast.title">{{ toast.title }}</div>
        <div class="toast-message">{{ toast.message }}</div>
      </div>
      <button class="toast-close" @click="remove(toast.id)">
        <i class="fa-solid fa-times"></i>
      </button>
      <div class="toast-progress" :style="{ animationDuration: toast.duration + 'ms' }"></div>
    </div>
  </transition-group>
</template>

<script>
export default {
  name: 'ToastNotification',
  data() {
    return {
      toasts: [],
      counter: 0
    }
  },
  methods: {
    show(options) {
      const toast = {
        id: ++this.counter,
        type: options.type || 'info',
        title: options.title || '',
        message: options.message || '',
        duration: options.duration || 4000
      }
      
      this.toasts.push(toast)
      
      // dps de duration remove o toast
      setTimeout(() => {
        this.remove(toast.id)
      }, toast.duration)
      
      return toast.id
    },
    
    success(message, title = '') {
      return this.show({ type: 'success', message, title })
    },
    
    error(message, title = '') {
      return this.show({ type: 'error', message, title, duration: 5000 })
    },
    
    warning(message, title = '') {
      return this.show({ type: 'warning', message, title })
    },
    
    info(message, title = '') {
      return this.show({ type: 'info', message, title })
    },
    
    remove(id) {
      const index = this.toasts.findIndex(t => t.id === id)
      if (index > -1) {
        this.toasts.splice(index, 1)
      }
    },
    
    getIcon(type) {
      const icons = {
        success: 'fa-solid fa-check-circle',
        error: 'fa-solid fa-times-circle',
        warning: 'fa-solid fa-exclamation-triangle',
        info: 'fa-solid fa-info-circle'
      }
      return icons[type] || icons.info
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 9998; /* z index aqui é pra garantir q vai ficar em cima do resto das coisa na tela */
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 380px;
}

.toast-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
  min-width: 300px;
}

.toast-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
  font-size: 1.1rem;
}

.toast-success .toast-icon {
  background: #d4edda;
  color: #155724;
}

.toast-error .toast-icon {
  background: #f8d7da;
  color: #721c24;
}

.toast-warning .toast-icon {
  background: #fff3cd;
  color: #856404;
}

.toast-info .toast-icon {
  background: #cce5ff;
  color: #004085;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.toast-message {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  word-wrap: break-word;
}

.toast-close {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 4px;
  margin-left: 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.toast-close:hover {
  background: #f0f0f0;
  color: #333;
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  width: 100%;
  animation: progress linear forwards;
}

.toast-success .toast-progress {
  background: #28a745;
}

.toast-error .toast-progress {
  background: #dc3545;
}

.toast-warning .toast-progress {
  background: #ffc107;
}

.toast-info .toast-progress {
  background: #007bff;
}

@keyframes progress {
  from { width: 100%; }
  to { width: 0%; }
}

/* Animações de entrada/saída */
.toast-enter-active {
  animation: slideIn 0.3s ease-out;
}

.toast-leave-active {
  animation: slideOut 0.2s ease-in;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideOut {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}

@media (max-width: 480px) {
  .toast-container {
    left: 10px;
    right: 10px;
    max-width: none;
  }
  
  .toast-item {
    min-width: auto;
  }
}
</style>

<template>
  <transition name="modal">
    <div v-if="visible" class="modal-overlay" @click.self="cancel">
      <div class="modal-container" :class="typeClass">
        <div class="modal-header">
          <div class="modal-icon">
            <i :class="iconClass"></i>
          </div>
          <h5 class="modal-title">{{ title }}</h5>
        </div>
        
        <div class="modal-body">
          <p>{{ message }}</p>
        </div>
        
        <div class="modal-footer">
          <button 
            class="btn btn-outline-secondary" 
            @click="cancel"
          >
            {{ cancelText }}
          </button>
          <button 
            class="btn" 
            :class="confirmBtnClass"
            @click="confirm"
          >
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'ConfirmModal',
  data() {
    return {
      visible: false,
      title: 'Confirmar',
      message: '',
      type: 'warning', // warning, danger, info, success
      confirmText: 'Confirmar',
      cancelText: 'Cancelar',
      resolvePromise: null,
      rejectPromise: null
    }
  },
  computed: {
    typeClass() {
      return `modal-${this.type}`
    },
    iconClass() {
      const icons = {
        warning: 'fa-solid fa-exclamation-triangle',
        danger: 'fa-solid fa-trash',
        info: 'fa-solid fa-info-circle',
        success: 'fa-solid fa-check-circle',
        question: 'fa-solid fa-question-circle'
      }
      return icons[this.type] || icons.warning
    },
    confirmBtnClass() {
      const classes = {
        warning: 'btn-warning',
        danger: 'btn-danger',
        info: 'btn-primary',
        success: 'btn-success',
        question: 'btn-primary'
      }
      return classes[this.type] || 'btn-primary'
    }
  },
  methods: {
    show(options = {}) {
      this.title = options.title || 'Confirmar'
      this.message = options.message || 'Você tem certeza?'
      this.type = options.type || 'warning'
      this.confirmText = options.confirmText || 'Confirmar'
      this.cancelText = options.cancelText || 'Cancelar'
      this.visible = true
      
      return new Promise((resolve, reject) => {
        this.resolvePromise = resolve
        this.rejectPromise = reject
      })
    },
    
    confirm() {
      this.visible = false
      if (this.resolvePromise) {
        this.resolvePromise(true)
      }
    },
    
    cancel() {
      this.visible = false
      if (this.resolvePromise) {
        this.resolvePromise(false)
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(2px);
}

.modal-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 400px;
  width: 90%;
  overflow: hidden;
  animation: modalIn 0.3s ease-out;
}

@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  padding: 24px 24px 16px;
  text-align: center;
}

.modal-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  font-size: 1.75rem;
}

.modal-warning .modal-icon {
  background: #fff3cd;
  color: #856404;
}

.modal-danger .modal-icon {
  background: #f8d7da;
  color: #721c24;
}

.modal-info .modal-icon {
  background: #cce5ff;
  color: #004085;
}

.modal-success .modal-icon {
  background: #d4edda;
  color: #155724;
}

.modal-question .modal-icon {
  background: #e2e3e5;
  color: #383d41;
}

.modal-title {
  margin: 0;
  font-weight: 600;
  color: #333;
}

.modal-body {
  padding: 0 24px 16px;
  text-align: center;
}

.modal-body p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.modal-footer {
  padding: 16px 24px 24px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.modal-footer .btn {
  min-width: 100px;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 500;
}

/* animações de entrada/saída */
.modal-enter-active {
  animation: fadeIn 0.2s ease-out;
}

.modal-leave-active {
  animation: fadeOut 0.15s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

.modal-leave-active .modal-container {
  animation: modalOut 0.15s ease-in;
}

@keyframes modalOut {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.9);
  }
}
</style>

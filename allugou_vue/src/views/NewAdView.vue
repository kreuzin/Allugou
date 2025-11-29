<template>
  <div class="container mt-4">
    <h2>Criar novo anúncio</h2>
    <p>Preencha as informações do item que deseja anunciar para locação.</p>
    
    <div class="card mt-4">
      <div class="card-body">
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label class="form-label">Título do anúncio</label>
            <input v-model="formData.titulo" type="text" class="form-control" required maxlength="50">
          </div>

          <div class="mb-3">
            <label class="form-label">Descrição</label>
            <textarea v-model="formData.descricao" class="form-control" rows="5" required maxlength="1500" placeholder="Descreva o item que você está oferecendo para locação..."></textarea>
            <small class="text-muted">{{ formData.descricao.length }}/1500 caracteres</small>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Valor da diária (R$)</label>
              <input v-model="formData.valorDiaria" type="number" step="0.01" class="form-control" required>
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Oferece entrega?</label>
              <select v-model="formData.ofereceEntrega" class="form-select" required>
                <option :value="true">Sim</option>
                <option :value="false">Não</option>
              </select>
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Imagens do produto *</label>
            <input 
              type="file" 
              class="form-control" 
              @change="handleFileChange" 
              multiple 
              accept="image/*"
              required
            >
            <small class="text-muted">Selecione uma ou mais imagens (obrigatório)</small>
          </div>

          <!-- preview das imagens -->
          <div v-if="imagePreviews.length > 0" class="mb-3">
            <label class="form-label">Pré-visualização das imagens</label>
            <div class="row g-2">
              <div v-for="(preview, index) in imagePreviews" :key="index" class="col-md-3">
                <div class="position-relative image-preview-container">
                  <img :src="preview" class="img-thumbnail" alt="preview">
                  <button 
                    type="button" 
                    class="btn btn-sm btn-danger position-absolute top-0 end-0 m-1"
                    @click="removeImage(index)"
                  >
                    <i class="fa fa-times"></i>
                  </button>
                  <div class="form-check mt-1">
                    <input 
                      class="form-check-input" 
                      type="radio" 
                      :name="'imagemPrincipal'" 
                      :id="'img-' + index"
                      :value="index"
                      v-model="imagemPrincipalIndex"
                    >
                    <label class="form-check-label small" :for="'img-' + index">
                      Imagem principal
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="text-center mt-4">
            <button type="submit" class="btn btn-primary me-2" :disabled="loading || imagePreviews.length === 0">
              {{ loading ? 'Salvando...' : 'Publicar anúncio' }}
            </button>
            <router-link to="/ads" class="btn btn-outline-secondary">Cancelar</router-link>
          </div>
        </form>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'NewAdView',
  data() {
    return {
      formData: {
        titulo: '',
        descricao: '',
        valorDiaria: '',
        ofereceEntrega: false
      },
      imageFiles: [],
      imagePreviews: [],
      imagemPrincipalIndex: 0,
      loading: false,
      error: null,
      success: null
    }
  },
  mounted() {
    // verificar se usuário é locador
    if (!this.$store.getters['auth/isLocador']) {
      this.$router.push('/')
    }
  },
  methods: {
    handleFileChange(event) {
      const files = Array.from(event.target.files)
      this.imageFiles = files
      this.imagePreviews = []
      
      // criar previews
      files.forEach(file => {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.imagePreviews.push(e.target.result)
        }
        reader.readAsDataURL(file)
      })
      
      // resetar imagem principal se necessário
      if (this.imagemPrincipalIndex >= files.length) {
        this.imagemPrincipalIndex = 0
      }
    },
    
    removeImage(index) {
      this.imageFiles.splice(index, 1)
      this.imagePreviews.splice(index, 1)
      
      // ajustar índice da imagem principal
      if (this.imagemPrincipalIndex >= this.imageFiles.length) {
        this.imagemPrincipalIndex = Math.max(0, this.imageFiles.length - 1)
      }
    },
    
    async handleSubmit() {
      this.loading = true
      this.error = null
      this.success = null

      try {
        // validar imagens
        if (this.imageFiles.length === 0) {
          this.error = 'Pelo menos uma imagem é obrigatória'
          this.loading = false
          return
        }
        
        // criar FormData para enviar com multipart/form-data
        const formData = new FormData()
        formData.append('titulo', this.formData.titulo)
        formData.append('descricao', this.formData.descricao)
        formData.append('valorDiaria', this.formData.valorDiaria)
        formData.append('ofereceEntrega', this.formData.ofereceEntrega)
        formData.append('imagemPrincipalIndex', this.imagemPrincipalIndex)
        
        // adicionar todas as imagens
        this.imageFiles.forEach(file => {
          formData.append('imagens', file)
        })
        
        // enviar requisição
        const response = await api.post('/api/ofertas/create/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        if (response.data.success) {
          this.success = 'Anúncio criado com sucesso!'
          
          setTimeout(() => {
            this.$router.push('/ads')
          }, 1500)
        } else {
          this.error = response.data.message || 'Falha ao criar anúncio'
        }
        
      } catch (err) {
        console.error('Erro ao criar anúncio:', err)
        this.error = err.response?.data?.message || 'Erro ao criar anúncio'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
}

.image-preview-container {
  position: relative;
}

.image-preview-container img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.image-preview-container .btn-danger {
  opacity: 0.9;
}

.image-preview-container .btn-danger:hover {
  opacity: 1;
}
</style>

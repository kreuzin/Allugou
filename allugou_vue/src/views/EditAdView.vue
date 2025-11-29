<template>
  <div class="container mt-4">
    <h2><i class="fa-solid fa-edit me-2"></i>Editar anúncio</h2>
    <p>Atualize as informações do seu anúncio.</p>
    
    <!-- loading inicial -->
    <div v-if="loadingOferta" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Carregando...</span>
      </div>
    </div>

    <!-- erro ao carregar -->
    <div v-else-if="loadError" class="alert alert-danger">
      {{ loadError }}
      <router-link to="/ads" class="btn btn-outline-danger btn-sm ms-3">Voltar</router-link>
    </div>

    <!-- formulário de edição -->
    <div v-else class="card mt-4">
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

          <!-- imagens existentes -->
          <div class="mb-3" v-if="imagensExistentes.length > 0">
            <label class="form-label">Imagens atuais</label>
            <div class="row g-2">
              <div v-for="img in imagensExistentes" :key="img.id" class="col-md-3">
                <div class="position-relative image-preview-container" :class="{ 'marked-remove': imagensParaRemover.includes(img.id) }">
                  <img :src="getImageUrl(img.imagem)" class="img-thumbnail" alt="imagem">
                  <button 
                    type="button" 
                    class="btn btn-sm position-absolute top-0 end-0 m-1"
                    :class="imagensParaRemover.includes(img.id) ? 'btn-success' : 'btn-danger'"
                    @click="toggleRemoveImage(img.id)"
                    :title="imagensParaRemover.includes(img.id) ? 'Restaurar' : 'Remover'"
                  >
                    <i :class="imagensParaRemover.includes(img.id) ? 'fa fa-undo' : 'fa fa-times'"></i>
                  </button>
                  <div class="form-check mt-1">
                    <input 
                      class="form-check-input" 
                      type="radio" 
                      name="imagemPrincipal"
                      :id="'existing-img-' + img.id"
                      :value="img.id"
                      v-model="imagemPrincipalId"
                      :disabled="imagensParaRemover.includes(img.id)"
                    >
                    <label class="form-check-label small" :for="'existing-img-' + img.id">
                      Imagem principal
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- adicionar novas imagens -->
          <div class="mb-3">
            <label class="form-label">Adicionar novas imagens</label>
            <input 
              type="file" 
              class="form-control" 
              @change="handleFileChange" 
              multiple 
              accept="image/*"
            >
            <small class="text-muted">Selecione imagens adicionais (opcional)</small>
          </div>

          <!-- preview das novas imagens -->
          <div v-if="imagePreviews.length > 0" class="mb-3">
            <label class="form-label">Novas imagens</label>
            <div class="row g-2">
              <div v-for="(preview, index) in imagePreviews" :key="'new-' + index" class="col-md-3">
                <div class="position-relative image-preview-container">
                  <img :src="preview" class="img-thumbnail" alt="preview">
                  <button 
                    type="button" 
                    class="btn btn-sm btn-danger position-absolute top-0 end-0 m-1"
                    @click="removeNewImage(index)"
                  >
                    <i class="fa fa-times"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- validação de imagens -->
          <div v-if="totalImagensRestantes === 0" class="alert alert-warning">
            <i class="fa fa-exclamation-triangle me-2"></i>
            Você precisa ter pelo menos uma imagem no anúncio.
          </div>

          <div class="text-center mt-4">
            <button 
              type="submit" 
              class="btn btn-primary me-2" 
              :disabled="loading || totalImagensRestantes === 0"
            >
              <i v-if="loading" class="fa fa-spinner fa-spin me-2"></i>
              {{ loading ? 'Salvando...' : 'Salvar alterações' }}
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
  name: 'EditAdView',
  data() {
    return {
      formData: {
        titulo: '',
        descricao: '',
        valorDiaria: '',
        ofereceEntrega: false
      },
      imagensExistentes: [],
      imagensParaRemover: [],
      imagemPrincipalId: null,
      imageFiles: [],
      imagePreviews: [],
      loadingOferta: true,
      loadError: null,
      loading: false,
      error: null,
      success: null
    }
  },
  computed: {
    totalImagensRestantes() {
      const existentesRestantes = this.imagensExistentes.filter(
        img => !this.imagensParaRemover.includes(img.id)
      ).length
      return existentesRestantes + this.imageFiles.length
    }
  },
  mounted() {
    // verificar se usuário é locador
    if (!this.$store.getters['auth/isLocador']) {
      this.$router.push('/')
      return
    }
    
    this.loadOferta()
  },
  methods: {
    async loadOferta() {
      this.loadingOferta = true
      this.loadError = null
      
      try {
        const ofertaId = this.$route.params.id
        const response = await api.get(`/api/ofertas/${ofertaId}/`)
        
        if (response.data.success) {
          const oferta = response.data.oferta
          
          this.formData = {
            titulo: oferta.titulo,
            descricao: oferta.descricao,
            valorDiaria: oferta.valorDiaria,
            ofereceEntrega: oferta.ofereceEntrega
          }
          
          this.imagensExistentes = oferta.imagens || []
          
          // definir imagem principal atual
          const principal = this.imagensExistentes.find(img => img.ehImagemPrincipal)
          if (principal) {
            this.imagemPrincipalId = principal.id
          } else if (this.imagensExistentes.length > 0) {
            this.imagemPrincipalId = this.imagensExistentes[0].id
          }
        } else {
          this.loadError = response.data.message || 'Erro ao carregar oferta'
        }
      } catch (err) {
        console.error('Erro ao carregar oferta:', err)
        this.loadError = err.response?.data?.message || 'Erro ao carregar oferta'
      } finally {
        this.loadingOferta = false
      }
    },
    
    getImageUrl(imagePath) {
      if (!imagePath) return null
      if (imagePath.startsWith('http')) return imagePath
      return `http://localhost:8000${imagePath}`
    },
    
    toggleRemoveImage(imgId) {
      const index = this.imagensParaRemover.indexOf(imgId)
      if (index > -1) {
        this.imagensParaRemover.splice(index, 1)
      } else {
        this.imagensParaRemover.push(imgId)
        
        // se removeu a imagem principal, selecionar outra
        if (this.imagemPrincipalId === imgId) {
          const proxima = this.imagensExistentes.find(
            img => !this.imagensParaRemover.includes(img.id)
          )
          this.imagemPrincipalId = proxima ? proxima.id : null
        }
      }
    },
    
    handleFileChange(event) {
      const files = Array.from(event.target.files)
      this.imageFiles = [...this.imageFiles, ...files]
      
      // criar previews
      files.forEach(file => {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.imagePreviews.push(e.target.result)
        }
        reader.readAsDataURL(file)
      })
    },
    
    removeNewImage(index) {
      this.imageFiles.splice(index, 1)
      this.imagePreviews.splice(index, 1)
    },
    
    async handleSubmit() {
      this.loading = true
      this.error = null
      this.success = null

      try {
        // validar imagens
        if (this.totalImagensRestantes === 0) {
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
        
        // IDs das imagens a remover
        if (this.imagensParaRemover.length > 0) {
          formData.append('removerImagens', this.imagensParaRemover.join(','))
        }
        
        // ID da imagem principal
        if (this.imagemPrincipalId) {
          formData.append('imagemPrincipalId', this.imagemPrincipalId)
        }
        
        // adicionar novas imagens
        this.imageFiles.forEach(file => {
          formData.append('imagens', file)
        })
        
        // enviar requisição
        const ofertaId = this.$route.params.id
        const response = await api.put(`/api/ofertas/${ofertaId}/edit/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        if (response.data.success) {
          this.success = 'Anúncio atualizado com sucesso!'
          
          setTimeout(() => {
            this.$router.push('/ads')
          }, 1500)
        } else {
          this.error = response.data.message || 'Falha ao atualizar anúncio'
        }
        
      } catch (err) {
        console.error('Erro ao atualizar anúncio:', err)
        this.error = err.response?.data?.message || 'Erro ao atualizar anúncio'
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
  transition: all 0.3s ease;
}

.image-preview-container img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.image-preview-container.marked-remove {
  opacity: 0.5;
}

.image-preview-container.marked-remove img {
  filter: grayscale(100%);
}

.image-preview-container .btn {
  opacity: 0.9;
}

.image-preview-container .btn:hover {
  opacity: 1;
}
</style>

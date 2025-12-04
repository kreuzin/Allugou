<template>
  <img :src="blobUrl || placeholder" :alt="alt" :class="imgClass" />
</template>

<script>
import axios from 'axios'

export default {
  name: 'NgrokImage',
  props: {
    src: {
      type: String,
      required: true
    },
    alt: {
      type: String,
      default: ''
    },
    imgClass: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23ddd" width="100" height="100"/%3E%3C/svg%3E'
    }
  },
  data() {
    return {
      blobUrl: null
    }
  },
  watch: {
    src: {
      immediate: true,
      handler(newSrc) {
        this.loadImage(newSrc)
      }
    }
  },
  beforeDestroy() {
    // limpa blob URL pra liberar memoria
    if (this.blobUrl) {
      URL.revokeObjectURL(this.blobUrl)
    }
  },
  methods: {
    async loadImage(url) {
      if (!url) return
      
      // se ja tem blob anterior, limpa
      if (this.blobUrl) {
        URL.revokeObjectURL(this.blobUrl)
        this.blobUrl = null
      }

      try {
        // faz fetch com header do ngrok
        const response = await axios.get(url, {
          responseType: 'blob',
          headers: {
            'ngrok-skip-browser-warning': 'true'
          }
        })
        
        // cria blob URL
        this.blobUrl = URL.createObjectURL(response.data)
      } catch (error) {
        console.error('Erro ao carregar imagem:', url, error)
      }
    }
  }
}
</script>

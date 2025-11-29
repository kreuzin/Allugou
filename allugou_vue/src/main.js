import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

//css e js do bootstrap importado globally pro projeto todo aq
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle'

// Componentes globais de UI
import ConfirmModal from './components/ConfirmModal.vue'
import ToastNotification from './components/ToastNotification.vue'

Vue.config.productionTip = false

// Criar instância do app
const app = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

// Plugin global para modais e toasts
const modalInstance = new Vue(ConfirmModal).$mount()
const toastInstance = new Vue(ToastNotification).$mount()

document.body.appendChild(modalInstance.$el)
document.body.appendChild(toastInstance.$el)

// Adicionar ao protótipo do Vue para acesso global
Vue.prototype.$confirm = (options) => modalInstance.show(options)
Vue.prototype.$toast = {
  show: (options) => toastInstance.show(options),
  success: (message, title) => toastInstance.success(message, title),
  error: (message, title) => toastInstance.error(message, title),
  warning: (message, title) => toastInstance.warning(message, title),
  info: (message, title) => toastInstance.info(message, title)
}

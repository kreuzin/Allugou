import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

//css e js do bootstrap importado globally pro projeto todo aq
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle'


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

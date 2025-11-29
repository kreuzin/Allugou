import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import auth from './modules/auth'
import notifications from './modules/notifications'

export default new Vuex.Store({
  modules: {
    auth,
    notifications
  }
})

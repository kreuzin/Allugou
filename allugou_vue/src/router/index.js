import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('../views/ForgotPasswordView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/ads',
    name: 'ads',
    component: () => import('../views/AdsView.vue'),
    meta: { requiresAuth: true, requiresLocador: true }
  },
  {
    path: '/new-ad',
    name: 'new-ad',
    component: () => import('../views/NewAdView.vue'),
    meta: { requiresAuth: true, requiresLocador: true }
  },
  {
    path: '/edit-ad/:id',
    name: 'edit-ad',
    component: () => import('../views/EditAdView.vue'),
    meta: { requiresAuth: true, requiresLocador: true }
  },
  {
    path: '/oferta/:id',
    name: 'oferta-detail',
    component: () => import('../views/OfertaDetailView.vue')
  },
  {
    path: '/requisicao/:id',
    name: 'requisicao-detail',
    component: () => import('../views/RequisicaoDetailView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/minhas-requisicoes',
    name: 'minhas-requisicoes',
    component: () => import('../views/MinhasRequisicoesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/minhas-locacoes',
    name: 'minhas-locacoes',
    component: () => import('../views/MinhasLocacoesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/locacao/:id',
    name: 'locacao-detail',
    component: () => import('../views/LocacaoDetailView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// guarda de navegação
router.beforeEach((to, from, next) => {
  // se o usuário autenticado tentar acessar login/register, redireciona para home
  if ((to.path === '/login' || to.path === '/register') && store.getters['auth/isAuthenticated']) {
    next({ path: '/' })
    return
  }

  // verificar se a rota requer autenticação
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters['auth/isAuthenticated']) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
    
    // verificar se a rota requer ser locador
    if (to.matched.some(record => record.meta.requiresLocador)) {
      if (!store.getters['auth/isLocador']) {
        next({
          path: '/',
          query: { error: 'acesso_negado' }
        })
        return
      }
    }
  }
  
  next()
})

export default router

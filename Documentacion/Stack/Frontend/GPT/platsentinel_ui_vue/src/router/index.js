import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../vistas/Dashboard.vue'
import Informes from '../vistas/Informes.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/informes', name: 'Informes', component: Informes }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
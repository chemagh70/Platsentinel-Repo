import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../vistas/Dashboard.vue'
import Informes from '../vistas/Informes.vue'
import Login from '../vistas/Login.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/informes', name: 'Informes', component: Informes },
  { path: '/login', name: 'Login', component: Login }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  if (to.name !== 'Login' && !token) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router
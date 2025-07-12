```javascript
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import InicioSesion from '../vistas/InicioSesion.vue';
import PanelPrincipal from '../vistas/PanelPrincipal.vue';
import Scans from '../vistas/Scans.vue';
import Reports from '../vistas/Reports.vue';
import Services from '../vistas/Services.vue';
import Learning from '../vistas/Learning.vue';

const routes = [
  { path: '/login', component: InicioSesion },
  { path: '/', component: PanelPrincipal, meta: { requiresAuth: true } },
  { path: '/scans', component: Scans, meta: { requiresAuth: true } },
  { path: '/reports', component: Reports, meta: { requiresAuth: true } },
  { path: '/services', component: Services, meta: { requiresAuth: true } },
  { path: '/learning', component: Learning, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
```
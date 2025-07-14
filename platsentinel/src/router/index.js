import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Dashboard from '../views/Dashboard.vue';
import EscaneoRed from '../views/EscaneoRed.vue';
import Tokens from '../views/Tokens.vue';
import DeteccionRiesgos from '../views/DeteccionRiesgos.vue';
import AnalisisVulnerabilidades from '../views/AnalisisVulnerabilidades.vue';
import GestionRiesgos from '../views/GestionRiesgos.vue';
import Herramientas from '../views/Herramientas .vue';

const routes = [
  { path: '/', component: Home },
  { path: '/dashboard', component: Dashboard },
  { path: '/herramientas', component: Herramientas  },
  { path: '/analisis-vulnerabilidades', component: AnalisisVulnerabilidades },
  { path: '/escaneo-red', component: EscaneoRed },
  { path: '/tokens', component: Tokens },
  { path: '/deteccion-riesgos', component: DeteccionRiesgos },
  { path: '/gestion-riesgos', component: GestionRiesgos }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
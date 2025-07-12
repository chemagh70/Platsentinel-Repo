// codigo_fuente/dashboard/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import PanelPrincipal from '../vistas/PanelPrincipal.vue';
import Scans from '../vistas/Scans.vue';
import Reports from '../vistas/Reports.vue';
import Services from '../vistas/Services.vue';
import Learning from '../vistas/Learning.vue';
import InicioSesion from '../vistas/InicioSesion.vue';

const routes = [
    { path: '/', component: PanelPrincipal },
    { path: '/scans', component: Scans },
    { path: '/reports', component: Reports },
    { path: '/services', component: Services },
    { path: '/learning', component: Learning },
    { path: '/login', component: InicioSesion }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
<template>
  <aside class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <div class="sidebar-header">
      <img src="@/assets/img/logo_r.png" alt="PlatSentinel Logo" class="logo" />
    </div>
    <nav>
      <router-link to="/" @click="isCollapsed = false" class="nav-item">Inicio</router-link>
      <router-link to="/dashboard" @click="isCollapsed = false" class="nav-item">Dashboard</router-link>
      <router-link to="/herramientas" @click="isCollapsed = false" class="nav-item">Herramientas</router-link>
      <router-link to="/escaneo-red" @click="isCollapsed = false" class="nav-item">Escaneo de Red</router-link>
      <router-link to="/tokens" @click="isCollapsed = false" class="nav-item">Tokens</router-link>      
      <router-link to="/analisis-vulnerabilidades" @click="isCollapsed = false" class="nav-item">Análisis de Vulnerabilidades</router-link>
      <router-link to="/deteccion-riesgos" @click="isCollapsed = false" class="nav-item">Detección de Riesgos</router-link>
      <router-link to="/gestion-riesgos" @click="isCollapsed = false" class="nav-item">Gestión de Riesgos</router-link>
    </nav>
    <div class="sidebar-footer">
      <button @click="$emit('toggle-sidebar')" class="toggle-btn">
        <img :src="isCollapsed ? './src/assets/img/flecha_r.png' : './src/assets/img/flecha_v.png'" alt="Toggle Sidebar" />
      </button>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  isCollapsed: Boolean
});

defineEmits(['toggle-sidebar']);
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #273623;
  color: #ecf0f1;
  transition: width 0.3s;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar-header {
  display: flex;
  justify-content: center;
  padding: 1rem;
  margin: 0;
}

.sidebar.collapsed .sidebar-header {
  justify-content: flex-start;
}

.logo {
  height: 40px;
  align-items: center;
  transition: filter 300ms;
}

.logo:hover {
  filter: brightness(1.2);
}

.sidebar-footer {
  margin-top: auto;
  padding: 0.5rem;
  text-align: right;
}

.sidebar.collapsed .sidebar-footer {
  text-align: left;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  margin: 0;
  padding: 0;
  outline: none;
}

.toggle-btn img {
  height: 20px;
  transition: transform 0.3s;
}

nav {
  padding: 2rem 0;
  margin: 0;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  text-align: left;
}

.nav-item {
  display: flex;
  justify-content: left;
  width: 100%;
  padding: 0.75rem 1rem;
  color: #ecf0f1;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s;
  margin: 0;
}

.nav-item:hover {
  background-color: #26520b;
}

.nav-item.router-link-active {
  background-color: #49a156;
}
</style>
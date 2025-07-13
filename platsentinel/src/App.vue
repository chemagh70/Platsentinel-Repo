<template>
  <!-- Contenedor principal que organiza la barra lateral y el contenido principal -->
  <div class="app-container">
    <!-- Barra lateral que contiene el logo y la navegación, con clase dinámica para colapsar -->
    <aside class="sidebar" :class="{ 'collapsed': isCollapsed }">
      <!-- Encabezado de la barra lateral con logo -->
      <div class="sidebar-header">
        <img src="./assets/logo_r.png" alt="PlatSentinel Logo" class="logo" />
      </div>
      <!-- Navegación con enlaces a las diferentes secciones, cada uno en una línea y centrado -->
      <nav>
        <router-link to="/" @click="isCollapsed = false" class="nav-item">Inicio</router-link>
        <router-link to="/dashboard" @click="isCollapsed = false" class="nav-item">Dashboard</router-link>
        <router-link to="/escaneo-red" @click="isCollapsed = false" class="nav-item">Escaneo de Red</router-link>
        <router-link to="/tokens" @click="isCollapsed = false" class="nav-item">Tokens</router-link>
        <router-link to="/deteccion-riesgos" @click="isCollapsed = false" class="nav-item">Detección de Riesgos</router-link>
        <router-link to="/analisis-vulnerabilidades" @click="isCollapsed = false" class="nav-item">Análisis de Vulnerabilidades</router-link>
        <router-link to="/gestion-riesgos" @click="isCollapsed = false" class="nav-item">Gestión de Riesgos</router-link>
      </nav>
      <!-- Botón de colapso/expansión en la parte inferior con imágenes -->
      <div class="sidebar-footer">
        <button @click="toggleSidebar" class="toggle-btn">
          <img :src="isCollapsed ? './src/assets/flecha_r.png' : './src/assets/flecha_v.png'" alt="Toggle Sidebar" />
        </button>
      </div>
    </aside>
    <!-- Contenido principal que se ajusta al espacio restante -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
  // Importar la referencia reactiva de Vue para manejar el estado de colapso
  import { ref, onMounted, onUnmounted } from 'vue';

  // Estado reactivo que controla si la barra lateral está colapsada
  const isCollapsed = ref(false);

  // Función para alternar el estado de colapso de la barra lateral
  function toggleSidebar() {
    isCollapsed.value = !isCollapsed.value;
  }

  // Función para actualizar el estado según el tamaño de la ventana
  function handleResize() {
    if (window.innerWidth <= 768) {
      isCollapsed.value = true; // Colapsa por defecto en móviles
    } else {
      isCollapsed.value = false; // Expande por defecto en pantallas grandes
    }
  }

  // Montar y desmontar el listener de redimensionamiento
  onMounted(() => {
    handleResize(); // Ajusta inicial al montar
    window.addEventListener('resize', handleResize);
  });

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
  });
</script>

<style scoped>
  /* Contenedor principal que usa flexbox para alinear sidebar y contenido */
  .app-container {
    display: flex;
    height: 100vh; /* Ocupa toda la altura de la ventana */
    margin: 0; /* Sin márgenes en el contenedor principal */
  }

  /* Estilo de la barra lateral, pegada a los bordes */
  .sidebar {
    width: 250px;
    background-color: #273623;
    color: #ecf0f1;
    transition: width 0.3s; /* Transición suave al colapsar */
    position: fixed; /* Fija la barra en su posición */
    top: 0; /* Pegada al borde superior */
    left: 0; /* Pegada al borde izquierdo */
    bottom: 0; /* Pegada al borde inferior */
    height: 100%; /* Ocupa toda la altura */
    margin: 0; /* Sin márgenes */
    padding: 0; /* Sin relleno interno */
    overflow: hidden; /* Evita desbordamiento */
    display: flex;
    flex-direction: column; /* Organiza los elementos en columna */
  }

  /* Estilo cuando la barra está colapsada */
  .sidebar.collapsed {
    width: 60px; /* Ancho reducido al colapsar */
  }

  /* Encabezado de la barra lateral con logo */
  .sidebar-header {
    display: flex;
    justify-content: center; /* Centra el logo horizontalmente */
    padding: 1rem;
    /* border-bottom: 1px solid #34495e; */
    margin: 0; /* Sin márgenes */
  }

  /* Ajuste del encabezado cuando la barra está colapsada */
  .sidebar.collapsed .sidebar-header {
    justify-content: flex-start; /* Alinea el logo a la izquierda cuando colapsada */
  }

  /* Estilo del logo dentro del encabezado */
  .logo {
    height: 40px; 
    align-items: center; /* Centra el logo verticalmente */
    transition: filter 300ms; /* Transición para efecto hover */
  }

  /* Efecto hover en el logo */
  .logo:hover {
    filter: brightness(1.2);
  }

  /* Pie de la barra lateral con el botón de colapso */
  .sidebar-footer {
    margin-top: auto; /* Empuja el botón al fondo */
    padding: 0.5rem;
    /* border-top: 1px solid #34495e; */
    text-align: right; /* Alinea el botón a la derecha cuando expandido */
  }

  /* Ajuste del pie cuando la barra está colapsada */
  .sidebar.collapsed .sidebar-footer {
    text-align: left; /* Alinea el botón a la izquierda cuando colapsada */
  }

  /* Botón de colapso en la parte inferior con imagen */
  .toggle-btn {
    background: none;
    border: none;
    cursor: pointer;
    margin: 0; /* Sin márgenes */
    padding: 0; /* Sin relleno */
    outline: none; /* Quita el marco al pulsar */
  }

  /* Imagen dentro del botón de colapso */
  .toggle-btn img {
    height: 20px; /* Ajusta el tamaño de la imagen según necesites */
    transition: transform 0.3s; /* Transición suave para rotación o movimiento */
  }

  /* Estilo de la navegación dentro de la barra */
  nav {
    padding: 2rem 0;
    margin: 0; /* Sin márgenes */
    flex-grow: 1; /* Ocupa el espacio disponible */
    display: flex;
    flex-direction: column; /* Cada enlace en una nueva línea */
    text-align: left; /* Alinea el texto a la izquierda */
  }

  /* Estilo de los enlaces de navegación como items individuales */
  .nav-item {
    display: flex;
    justify-content: left; /* Alinea el texto a la izquierda */
    width: 100%;
    padding: 0.75rem 1rem;
    color: #ecf0f1;
    text-decoration: none;
    font-weight: 500;
    transition: background-color 0.3s;
    margin: 0; /* Sin márgenes */
  }

  /* Efecto hover en los enlaces */
  .nav-item:hover {
    background-color: #34495e;
  }

  /* Estilo del enlace activo */
  .nav-item.router-link-active {
    background-color: #3498db;
  }

  /* Contenido principal que se ajusta al espacio */
  .main-content {
    margin-left: 250px; /* Espacio para la barra lateral */
    padding: 2rem;
    width: calc(100% - 250px);
    transition: margin-left 0.3s, width 0.3s;
    margin-top: 0; /* Sin margen superior */
    margin-bottom: 0; /* Sin margen inferior */
  }

  /* Ajuste del contenido cuando la barra está colapsada */
  .sidebar.collapsed + .main-content {
    margin-left: 60px;
    width: calc(100% - 60px);
  }

  /* Media query para pantallas menores a 768px (móviles) */
  @media (max-width: 768px) {
    /* Ajusta la barra lateral para que sea colapsada por defecto */
    .sidebar {
      width: 60px; /* Ancho colapsado por defecto */
      transition: width 0.3s;
    }

    .sidebar.collapsed {
      width: 250px; /* Expande al colapsar en móviles */
    }

    .main-content {
      margin-left: 60px;
      width: calc(100% - 60px);
    }

    .sidebar.collapsed + .main-content {
      margin-left: 250px;
      width: calc(100% - 250px);
    }
  }

  /* Media query para tablets (768px a 1024px) */
  @media (min-width: 768px) and (max-width: 1024px) {
    .sidebar {
      width: 250px; /* Barra expandida en tablets */
    }

    .sidebar.collapsed {
      width: 60px; /* Ancho reducido al colapsar */
    }

    .main-content {
      margin-left: 250px;
      width: calc(100% - 250px);
    }

    .sidebar.collapsed + .main-content {
      margin-left: 60px;
      width: calc(100% - 60px);
    }
  }

  /* Media query para pantallas grandes (más de 1024px) */
  @media (min-width: 1025px) {
    .sidebar {
      width: 250px; /* Barra expandida en pantallas grandes */
    }

    .sidebar.collapsed {
      width: 60px; /* Ancho reducido al colapsar */
    }

    .main-content {
      margin-left: 250px;
      width: calc(100% - 250px);
    }

    .sidebar.collapsed + .main-content {
      margin-left: 60px;
      width: calc(100% - 60px);
    }
  }
</style>
<template>
  <div class="container">
    <h1>📊 Dashboard SentinelCore</h1>
    <p>Bienvenido, selecciona una opción:</p>
    <router-link to="/informes">📄 Ver Informes</router-link>
    <br/>
    <a href="#" @click="logout">🔓 Cerrar sesión</a>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  methods: {
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  }
}
</script>
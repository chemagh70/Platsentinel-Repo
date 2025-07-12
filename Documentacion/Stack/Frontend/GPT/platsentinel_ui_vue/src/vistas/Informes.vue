<template>
  <div>
    <h2>📄 Informes disponibles</h2>
    <ul>
      <li v-for="informe in informes" :key="informe.nombre">
        {{ informe.nombre }}
        <a :href="informe.url" target="_blank">📥 Descargar</a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Informes",
  data() {
    return {
      informes: []
    };
  },
  mounted() {
    fetch("http://localhost:8000/resultados/listar-informes", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    })
      .then(res => res.json())
      .then(data => {
        this.informes = data
      })
  }
}
</script>
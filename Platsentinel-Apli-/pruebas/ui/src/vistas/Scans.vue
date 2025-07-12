```vue
<!-- src/vistas/Scans.vue -->
<template>
  <div>
    <h1 class="text-3xl font-bold mb-4">Escaneos</h1>
    <button @click="iniciarEscaneo" class="bg-green-500 text-white p-2 rounded hover:bg-green-600">Iniciar Nuevo Escaneo</button>
    <TablaResultados :headers="['ID', 'Fecha', 'Estado']" :data="scans" />
  </div>
</template>

<script>
import TablaResultados from '../componentes/TablaResultados.vue';
import axios from 'axios';

export default {
  components: {
    TablaResultados,
  },
  data() {
    return {
      scans: [
        { id: 1, fecha: '2025-07-11', estado: 'Completado' },
        { id: 2, fecha: '2025-07-10', estado: 'En Progreso' },
      ],
    };
  },
  methods: {
    async iniciarEscaneo() {
      const response = await axios.post('http://localhost:8000/scans', {});
      this.scans.push({ id: this.scans.length + 1, fecha: new Date().toISOString().split('T')[0], estado: 'En Progreso' });
    },
  },
};
</script>
```
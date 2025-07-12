```vue
<!-- src/vistas/Reports.vue -->
<template>
  <div>
    <h1 class="text-3xl font-bold mb-4">Informes</h1>
    <TablaResultados :headers="['ID', 'Fecha', 'Descarga']" :data="reports" />
  </div>
</template>

<script>
import TablaResultados from '../componentes/TablaResultados.vue';

export default {
  components: {
    TablaResultados,
  },
  data() {
    return {
      reports: [
        { id: 1, fecha: '2025-07-11', descarga: 'Descargar' },
        { id: 2, fecha: '2025-07-10', descarga: 'Descargar' },
      ],
    };
  },
};
</script>
```
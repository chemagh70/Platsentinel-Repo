```vue
<!-- src/vistas/Services.vue -->
<template>
  <div>
    <h1 class="text-3xl font-bold mb-4">Servicios</h1>
    <TablaResultados :headers="['ID', 'Nombre', 'Estado']" :data="services" />
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
      services: [
        { id: 1, nombre: 'OWASP ZAP', estado: 'Activo' },
        { id: 2, nombre: 'ClamAV', estado: 'Inactivo' },
      ],
    };
  },
};
</script>
```
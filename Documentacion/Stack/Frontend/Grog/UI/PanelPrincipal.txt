```vue
<!-- src/vistas/PanelPrincipal.vue -->
<template>
  <div>
    <h1 class="text-3xl font-bold mb-4">Panel Principal</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <TarjetaResumen title="Escaneos Realizados" value="25" />
      <TarjetaResumen title="Informes Generados" value="15" />
      <TarjetaResumen title="Servicios Activos" value="10" />
    </div>
  </div>
</template>

<script>
import TarjetaResumen from '../componentes/TarjetaResumen.vue';

export default {
  components: {
    TarjetaResumen,
  },
};
</script>
```
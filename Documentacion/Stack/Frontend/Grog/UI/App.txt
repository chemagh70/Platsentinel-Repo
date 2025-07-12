```vue
<!-- src/App.vue -->
<template>
  <div>
    <BarraNavegacion />
    <div class="container mx-auto p-4">
      <router-view />
    </div>
  </div>
</template>

<script>
import BarraNavegacion from './componentes/BarraNavegacion.vue';

export default {
  components: {
    BarraNavegacion,
  },
};
</script>
```
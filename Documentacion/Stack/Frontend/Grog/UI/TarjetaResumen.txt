```vue
<!-- src/componentes/TarjetaResumen.vue -->
<template>
  <div class="bg-white p-4 rounded-lg shadow-md text-center">
    <h3 class="text-lg font-semibold">{{ title }}</h3>
    <p class="text-2xl mt-2">{{ value }}</p>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    value: String,
  },
};
</script>
```
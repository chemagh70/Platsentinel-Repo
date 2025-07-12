```vue
<!-- src/componentes/TablaResultados.vue -->
<template>
  <div class="mt-4">
    <table class="min-w-full bg-white border border-gray-300">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header" class="py-2 px-4 border-b">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="index" class="hover:bg-gray-100">
          <td v-for="cell in row" :key="cell" class="py-2 px-4 border-b">{{ cell }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    headers: Array,
    data: Array,
  },
};
</script>
```